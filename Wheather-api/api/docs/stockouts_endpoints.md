[BACK](../stockouts.md#Stock-outs)

# Order Integration API
## Menus (Internal)
```
[POST Stockouts](/api/v3.6/internal/locations/{locationId}/menus/stockouts)
```
- The process where items that are 86’d at the store are to be removed from the GH menu so that it isn’t mistakenly ordered.
- An internal endpoint that update the stockouts to the provider.

**Path Parameters:**
* `locationId` - integer (required) | The Qu location identifier.

**Query Parameters:**
* `forceStockoutUpdate` - boolean (default value: false) | if set to true - [force stockout update].

**Example Request:**

```
curl -X 'POST' \'<base_url>/api/v3.6/internal/locations/{locationId}/menus/stockouts?forceStockoutUpdate=false' \-H 'accept: */*' \-d ''
```

```
200 OK
```

[BACK](../stockouts.md#Stock-outs)