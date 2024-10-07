[BACK](../README.md#menus-mapping)

## Taxes
- Two types of taxes are applied to any item on the menu.
- Item-level tax rates that are included in the normalized menu structure.
- Store-level tax rates is the overall tax rates for a merchant.
- Grubhub does not calculate store-level taxes for an item if it already has an item-level tax associated with it.           
- If an item has both item-level as well as store-level tax, then we are combining them and sending.

### Item-level tax
- The applicable taxes for an item are assigned based on the configuration in Qu.
- So, items are properly taxed when orders are created and priced on the GH platform.
- We add up all of the applicable tax rates for each item from the Qu menu.
- If an item has item-level tax associated, we check the total store-level tax percentage and set, it if the total percentage > 0.
- Finally, we create a tax rate using store-level and item-level tax calculation.
- For efficiency, If another tax_rate already exists with the same total rate applied, we use the existing reference instead of creating a new tax_rate.
- When the item is synced to Grubhub, then that tax_rate is assigned to the item or modifier.

### Model Structure
- The tax rate is applied for each item and modifier on the menu.

```
{
  "external_id": <string>,
  "name": <string>,
  "rate": <double>
}

external_id - The merchant-set ID for the tax rate, which can be used to link it in the GrubhubNormalizedMenu's items and modifiers.
name - The name of the tax rate.
rate - The decimal tax rate value that must be between 0 and 1.
```

### Approach
- We create a taxTypeLookups that contains all the configured taxes of Qu.
- The Qu menu has the applicable tax property for the item.
- We calculate the tax_rate with the item's applicable tax IDs with taxTypeLookups and accordingly create the tax rate model.

### Example
1. We have an item with 3 applicable taxes (ex. 2 (2%), 3 (3%), 4 (4%)%).
    - We create a tax rate as mention below.

    ```
        "tax_rates": [
        {
            "external_id": "2_3_4_tax",
            "name": "2_3_4_tax",
            "rate": 0.09
        }
    ```

    - When the item is synced to Grubhub, then the tax rate for that item is set to be ```"2_3_4_tax"``` which represents the ```0.09``` tax rate.
    - Here, we also check the total store-level tax percentage and update the tax rate with store-level tax.
    - For example if store-level tax = 5 (5%), then updated tax rate = ```"2_3_4_5_tax"``` which represent the ```0.14``` tax rate.

2. We have an item priced at $10 with one applicable tax (ex. 1 (5%)) and it has a priced child modifier priced at $1 with a tax rate of 2 (2%).
    - We create a tax rate as mention below.

    ```
        "tax_rates": [
        {
            "external_id": "1_tax",
            "name": "1_tax",
            "rate": 0.05
        },
        {
            "external_id": "2_tax",
            "name": "2_tax",
            "rate": 0.02
        }
    ```

    - When the item is synced to Grubhub, then the tax rate for that item is set to be "1_tax" and for modifier is "2_tax".
    - So, The tax rate should be calculated as 0.5 for the main item and 0.02 for the child item.
    - Grand total price = (10 + 0.5) + (1 + 0.02) = $11.52.

   
### Store-level tax
- Store-level tax is the overall tax rate for a merchant. 
- These rates will be used for any menu item that does not have its tax rate configuration.
- We consider the taxes for which the tax's trigger item type is applied for AllBaseItems based on the configuration in Qu.
- Store-level tax rates are set via the Update Tax Rates API.


### End Point

```
To get the overall tax rates for a merchant.
GET - /pos/v1/merchant/{merchant_id}/taxrate

To update the overall tax rates for a merchant
PUT - /pos/v1/merchant/{merchant_id}/taxrate

merchant_id - The merchant id corresponds to a single location.
```

- To update the overall tax rates for a merchant, we need to send a body schema as - 
```
{
  "rate": <double>
}

rate - The default tax rate that apply to all menu items associated with this merchant.
```

### Example
- If there are two taxes defined for store-level - ex - 1%, 3%
- When the item of price $10 is synced to Grubhub - the overall tax applied to the item is 0.4.
- So, the total price is 10 + 0.4 = 10.4

### Additional References:
 - [Sequence Diagram: Item-Level Tax](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G15N-k5v98cA2v-DAfpqrhmeels4yLKnCJ)
 - [Sequence Diagram: Store-Level Tax](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1LebfRV7AFS9BjU1hz2acvuOMX2izd7Nf)
 - [Documentation: Store-Level Tax](https://developer.grubhub.com/api/merchant-data#tag/Endpoints/operation/getMerchantTaxRate)
 - [Documentation: Item-Level Tax](https://developer.grubhub.com/docs/pr1nKPTJ0x1Gx7eHyZf6C/creating-menus)

 [BACK](../README.md#menus-mapping)
