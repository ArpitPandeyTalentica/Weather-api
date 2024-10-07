[BACK](../menus.md#menu-mapping)

## Stock-outs

- The process where items that are 86’d at the store are to be removed from the GH menu so that it isn’t mistakenly ordered.
- The process is only applicable when menu sync to grubhub is complete i.e status should be in complete state.
- This applies for Grubhub - Item, modifier and portion type item.

**Note** 
If all portions of an item are out of stock then the main item should be considered out of stock.

**End Point**
The endpoint that allows for “scheduling override” updates in bulk which is stated to be used for 86’ing.

```
PATCH - pos/v1/merchant/{merchantId}/menu/schedules/overrides/external?allow_partial_success={true/false}

To get job status :- GET - pos/v1/merchant/{merchantId}/menu/schedules/overrides/{job_id}/status

job_id - reponse property from PATCH api call.

To get latest menu : - GET - /pos/v1/merchant/{merchantId}/menu/normalized

```

To update the availability of the item we need to send GrubhubScheduleOverrideBaseRequest - :
```
{
    "GrubhubScheduleOverrideBaseRequest": {
        "entity_ids" : <Collection of string>
        "schedule_override": {
            "op": <string>,
            "cur_end_date": <string>,
            "start-date": <string>,
            "end-date": <string>,
            "show_or_hide": <string>
        }
    }
}
```

op - The operation to perform [ADD, UPDATE].

cur_end_date - For UPDATE operations, this field is required, otherwise it is not.

start - The beginning of the override period.

end - The end of the override period. Example -  "9999-12-31T23:59:00.000Z"

show_or_hide - The options to use for the override - SHOW/HIDE.

**To Notify The Grubhub -**

1. We fetch the latest stock data from EI via Inventory repository.
2. We then fetch the latest stocked out items data saved in the IntegrationStockout collection.
3. We then compare the current stock data and the existing stocked out items data to determine if the stockout process should be initiated. If the “forceStockoutUpdate” flag is true then we initiate the stockout process regardless of the stock data.
4. If stockout is required then we fetch the latest stocked out items at Grubhub by filtering "UNAVAILABLE" items from availability overrides from the currently synced Grubhub menu and also create a set of external ids of items that have a override present in the menu.
5. Then we fetch the latest Grubhub menu and we iterate over all the Grubhub MenuItem, modifier and Portion type Items.
6. We check every item against the current stock data and existing stocked out items data to determine if we need to stock-in/out the item.
7. Create a separate list for items to be stocked out and stocked in.
8. Once we have iterated over all the items in menu, we check if the total items to be processed (stock-out/in) are more than the Throttling limit for the Grubhub bulk schedule override API.
9. If the total items to be processed are less than the throttling limit then we create an array which contains the ADD/UPDATE override requests.
10. If the total items to be processed are greater than the throttling limit, then we set a flag “InitiateStockoutOnCompletion” to true and select items up to the throttling limit and create request for them.
11. We then invoke the Bulk Schedule override API and save the job details in DB with the “InitiateStockoutOnCompletion” flag.
12. If there are no items to be stocked-out/in after checking all items/modifiers in dictionary, we update the existing stocks in the database with the stock data fetched from Grubhub. 

Note - 1. For the end date, we are using a fixed date as  - 200 years future date **example -  "2200-01-01T00:00:00.000Z"**
     - 2. For 86's the item  - Start date is set as Now and end date is a fixed date mention in **step 1**
     - 3. For Un86's the item - end date should be that fixed date of 86's operation and also a other column curr_end_date set same as end date.
     - 4. Throttling limit is set as 99. Per request will goes for a maximum 99 items.
     - 5. Also, we are setting the **allow_partial_success** flag to true, so if for any item in the request the override operation fails, the rest will still be processed.

**Item availability dictionary preparation approach that we have mentioned above (To Notify The Grubhub->step 1)**
-  Created using 
   - 1. Currently configured stock outs - ItemStock
   - 2. QuItemStocks from IntegrationStockouts table
-  If there is no changes in QuItemStocks and current configure stock outs, then the both list are equal by matching their respective ItemMasterId, portionTypeId and now dictionary is empty.
-  Else it is adding all the current configured stock outs data with **availability = false**.
-  Then also it is trying to find the previous stocked-out item from the Current configured stock outs items.
-  Basically it is checking if the currently configured item list doesn't contain the previous stocked out item by matching their respective ItemMasterId, portionTypeId. Then that previous stocked out item add to the dictionary with **availability = true**

 **Approach**: 
1. We are using two lists of item to save that is in the IntegrationStockouts Table - 
2. QuItemStock - Current Stocked-out Item, PreviousQuItemStock - Previous Stocked-out Item
3. First time when we configure the item to stocked-out (86ing) in EI, Current Item that stocked out saved by QuItemStock and again when we back in stock the item,then previous history saved by PreviousQuItemStock.

**Example -**

1. Initially - item1,item2 - set as out of stock  - It goes to ItemStock - 
- QuItemStock - 2
- PreviousQuItemStock - 0

2. If Item1 - set as back in stock,
QuItemStock - 1 - item2
PreviousQuItemStock - 2 (item1,item2)

2. Again if we set item2 as In-Stock to other item then - It goes to PreviousItemStock
QuItemStock - 0
PreviousQuItemStock - 1 (item2)

**Webhook Update Job-Staus Approach**
1. This is used to receive schedule override job status when updating stock out info at Grubhub.
2. In the process of stockout, we are calling Grubhub api with request - List of Entity_id and Schedule Override data - **Model Structure and Grubhub api mentioned on top**
3. Then we are saving the data in Db -> GrubhubIngestionJobDetails, as per job_id (from the step-2 response) with processingComplete = false.
4. Update the db (Integrationstockout) with stockout items, InProgress status and save.
5. Then we wait for Webhook response - Below is the sample webhook response.
``` 
{
    "job_id": <string>,
    "processing_complete": <boolean>,
    "status": "SUCCESSFUL" / "FAILED",
    "entity_override_results" : Individual entity override status
} 
```
6. Then we are fetching the job details from db (GrubhubIngestionJobDetails) for this job id, 
7. Update the processingComplete with true and save.
8. Then we are fetching all "UNAVAILABLE" availability override from grubhub api call and converting to ItemStock collection.
```
    GET - pos/v1/merchant/{merchant_id}/menu/normalized
```
11.Finally compares the current stockout data in db with the stockout data from job responses and Grubhub menu availability_overrides and updates the stocked out item data in db (Integrationstockout), complete the status and save.
12. If the “InitiateStockoutOnCompletion” flag saved with the job details is true then we initiate another Stockout process with “forceStockoutUpdate” flag set to true, this will cover the remaining items that were not considered in the previous stockout process (due to total items > Throttling Limit).

Additional References:
 - [Data Flow Diagram: Stockout](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1f7lkCsK1MSgNI5IlK30CX8tC0XxnXaHX)
 - [Grubhub-Webhook Flow Diagram: Stockout](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1AWB_PdEUSBoVHr3wQ-DANySk1HUtjC71)
 - [Documentation:](https://developer.grubhub.com/api/menu#tag/Models/PosScheduleOverrideBaseRequest) 

 [BACK](../menus.md#menu-mapping)
