[BACK](../order_integrations.md#introduction)

# Grubhub Integration Documentation
## Contents
* [Background](#background)
* [Grubhub API](#grubhub-api)
* [Provider Configurations](#provider-configurations)
* [Menu Mapping](#menus-mapping)
* [Process Orders](#process-orders)
* [Documentation](#documentations-and-api)


## Background
- Grubhub’s Partner Integration API enables a merchant’s Point-of-sale, third-party online-ordering provider, or the merchant themselves to seamlessly manage menus and Grubhub orders within their existing operational workflows. 
- The end results of an effective integration include increased operational efficiency for the merchant and improved service levels to customers. 
- Integration functionality includes:
   - Menu creation, ingestion, and updates
   - Order handling and status
   - Delivery information
   - Stockouts
   - Tags & Taxes

## Grubhub API

### Authentication
- Grubhub utilises two different authentication schemes for authenticating requests from Qu to Grubhub and Grubhub to Qu.
- For calls from Qu to Grubhub, the request must contain two specific header with the required parameters.
- For calls from Grubhub to Qu webhooks, Qu expects a valid JWT in the authorization header.


### Documentations and API
* [Authorization](authorization/authorization.md##Authentication-for-Grubhub-Integration)
* [Configiration](configurations/configurations.md#Grubhub-Integration-Documentations)
* [Diagnostics](diagnostics/diagnostics.md#Diagnostics)
* [Menus](menus/menus.md##Menu-Mapping)
* [Merchant Schedule](merchant_schedule/merchant_schedules.md##Merchant-Schedules)
* [Orders](orders/process_orders.md##Order-Injection)

## Provider Configurations
* [Grubhub Provider Configurations](configurations/configurations.md#Grubhub-Integration-Documentations)

## Menus Mapping
* [Menu Mapping](menus/menus.md##Menu-Mapping)

### See also:
* [Custom Tags](menus/custom_tag.md##Custom-Tag-Support)
* [Stockouts](menus/stockouts.md##Stock-outs)
* [Menu Taxes](menus/taxes.md##Taxes)


## Process Orders
### Flow:
- The order injection flow allows for retrieving and managing orders placed for a given location.
- New orders are identified by filtering for the `RESTAURANT_CONFIRMABLE` status.
- Future orders are identified by filtering for the `ANTICIPATED` status.
- We are not handling future orders, as we get second notification when order is `RESTAURANT_CONFIRMABLE`.
- We are ignoring test orders based on `is_test` property.


### See also:
* [Process Order](orders/process_order.md##Order-Injection)
* [Pre Order Validation](orders/validate_order.md##Pre-Order-Webhook-Validation)
* [Documentation: Order Validation](https://developer.grubhub.com/docs/1DsR8UxjrosdOZoC5eVyhy/order-validation)

[BACK](../order_integrations.md#introduction)