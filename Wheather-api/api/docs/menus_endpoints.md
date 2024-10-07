[BACK](../menus.md#menu-mapping)

# Order Integration API
## Menus (Internal)
```
[POST Process the location menu](/api/v3.6/internal/locations/{locationId}/menus)
```
- An internal endpoint that generates the menu and saves the menu mapping in the background as preparation for Grubhub order injection.

**Path Parameters:**
* `locationId` - integer (required) | The Qu location identifier.

**Query Parameters:**
* `forceMenuUpdate` - boolean (default value: false) | if set to true - [force menu update].

**Example Request:**

```
curl -X 'POST' \'<base_url>/api/v3.6/internal/locations/{location_id}/menus?forceMenuUpdate=false' \-H 'accept: */*' \-d ''
```

```
200 OK
```

[BACK](../menus.md#menu-mapping)