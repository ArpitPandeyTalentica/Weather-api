## Merchant Schedules
- The merchant schedules component allows us to manage a restaurant's hours of operation. 
- This includes the day-to-day pickup and delivery hours, as well as schedule overrides. 
- Schedule overrides are used to manage holiday hours and intra-day hours changes.
### Store Hours
- Store hours are set as business hours in EI and with the menu sync call, the store hours for the location are sent to Grubhub.
- Store hours for GrubHub are  set based on the context configured in the platform settings.
- Store hours are accepted as a repeating weekly schedule for time range.
- Store hours are defined same for both PICKUP and DELIVERY.
- For Example - the store hours to be 10AM to 10PM, the Grubhub only allow orders until 10:00PM.

### End Point
```
1. Creates a merchant schedule for delivery and pickup schedules.
   PUT /pos/v1/merchant/{merchant_id}/schedules/repeating

2. Gets a merchant's schedules.
   GET /pos/v1/merchant/{merchant_id}/schedules/repeating

   merchant_id - The Grubhub id for the merchant that Corresponds to a single location.
```
- To update the store hours for the Grubhub, we need to send a body schema as - 
```
{
  "source": <string>,
  "intervals": <array of object>,
  "schedule_type": <string>
}
source - The source of the create or update of the repeating schedule.
intervals - Array of the schedule of the day of the week within a schedule update request.
schedule_type - Type of repeating schedule i.e. DELIVERY, PICKUP, and CATERING.
```
### Holiday/Special hours
- Store hours include a special setting for holidays/special dates with custom times.
- Holidays/special store hours set on EI to be sync�d to GrubHub so that the store doesn�t appear to be open or close.
- Holiday/Special hours are defined same for both PICKUP and DELIVERY.
- Grubhub uses `schedule overrides` to set up custom holidays and special hours for current or future dates.

### Outcomes of holiday/Special hours
- If the store is closed for a holiday, then the schedule override is set to be UNAVAILABLE with a start/end date to cover the entire 24-hour period of that day.
- If the store has updated hours, then the schedule override is set to be AVAILABLE with the start/end date to cover the time range specified in EI.

### End Point
```
1. Retrieve all schedule overrides for a merchant.
   GET /pos/v1/merchant/{merchant_id}/schedules/overrides

2. Add a schedule override for a merchant.
   POST /pos/v1/merchant/{merchant_id}/schedules/overrides

3. Delete the existing schedule override for a merchant.
   DELETE /pos/v1/merchant/{merchant_id}/schedules/overrides

   merchant_id - The Grubhub id for the merchant that Corresponds to a single location.
```
- To add a schedule override for a merchant, we need to send a body schema as - 
```
{
  "start": <string-dateTime>,
  "end": <string-dateTime>,
  "type": <string>,
  "schedule_name": <string>
}
start - Start time of the override duration in the merchant's local time.
end - End time of the override duration in the merchant's local time.
type - Type of schedule override. "UNAVAILABLE" is a duration when the merchant should be closed, when normally they would be open. "AVAILABLE" is a duration when the merchant should be open, when normally they would be closed.
schedule_name - Standard types of schedules - "DELIVERY" "PICKUP"
```
- To delete a schedule override for a merchant, we need to send a body schema as - 
```
{
  "current_end_time": <string-dateTime>,
  "type": <string>
}
current_end_time - Current end time of the override to be deleted. Used as reference for the override.
type - Type of schedule override. "UNAVAILABLE" is a duration when the merchant should be closed, when normally they would be open. "AVAILABLE" is a duration when the merchant should be open, when normally they would be closed.
```
### Algorithm approach
- Using an algorithm approach, we get the available or unavailable slots for special hours in-store hours
- To find the UNAVAILABLE slot for special hour.
  - We find the gap of special hours in full day slot and then take intersection with store hours.
- To find the AVAILABLE slot for special hour.
  - We find the gap of store hours in full day slot and then take intersection with special hours.
### Algorithm
- Steps to find slots for two list of specialHours and StoreHours.
```
List<Hours> storeHourSlots, List<Hours> specialHourSlots.
```
1. Firstly we are sorting the time range with their opening time.
2. Initialize a results list and a full day slots.
3. Execute the loop till the special hour slots.
4. Calculates the intersected slots between the regular store hours (storeHourSlots) and the slots in the results list

### Example
1. Store hours = 00:00 to 23:59 and Special Hours = 10:00 to 14:00 and 17:00 to 22:00
   Then Request sent to Grubhub to open the store between special hours
     a. UNAVAILABLE Requests - 00:00 to 10:00, 14:00 to 17:00, 22:00 to 23:59
     b. AVAILABLE Requests - No need to send
   
2. Store hours = 10:00 to 14:00, 16:00 to 18:00, 20:00 to 22:00 and Special Hours = 11:00 to 12:00 and 15:00 to 17:00
   Then Request sent to Grubhub to open the store between special hours
     a. UNAVAILABLE Requests - 10:00 to 11:00, 12:00 to 14:00, 17:00 to 18:00, 20:00 to 22:00
     b. AVAILABLE Requests - 15:00 to 16:00

### Threshold Limit Scenario
- Grubhub allows only up to 100 scheduled overrides to add for holiday/special hours.
- After adding 100 overrides, Grubhub doesn't allow to add more schedule overrides.
- So, when we try to add another schedule override, POST API throws an error.

## Threshold limit handling approach
- We are deleting past applied overrides before any action.
- We are making sure to push the earliest overrides and delete the future ones to make room for the threshold limit.
- We are creating the delete request from existing schedule overrides for the extra set of override requests that remain after the threshold limit.
- Basically, we sort the existing overrides in descending order based on their local end dates. 
- If the existing override's end date is later, we create a request to delete for it.
- If there is no room to delete then we are logging them as we are not able to add those requested overrides.
                            
### Additional References:
 - [Sequence Diagram: Holiday/Special Hours](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1F8EeNHeHNM5WzmdPV7_NfpTwl05n1wUL)
 - [Documentation:](https://developer.grubhub.com/api/merchant-schedules#tag/Endpoints/operation/putRepeatingSchedule)
