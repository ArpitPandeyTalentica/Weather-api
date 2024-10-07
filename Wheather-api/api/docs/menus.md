[BACK](../README.md#menus-mapping)

## Menu Mapping

### Assumptions:
Grubhub menu only supports up to 21 levels.

Take an example below:

**Qu Menu**
```
LVL1 +-- Menu
LVL2 +---- Category
LVL3 +------ Item_1
LVL4 +-------- ItemGroup_1
LVL5 +---------- Item_2
LVL5 +---------- Item_3
LVL6 +------------ ItemGroup_2
LVL7 +-------------- Item_4
LVL7 +-------------- Item_5
LVL8 +---------------- ItemGroup_3
LVL9 +------------------ Item_6
LVL10 +-------------------- ItemGroup_4
LVL11 +---------------------- Item_7
LVL12 +------------------------ ItemGroup_5
LVL13 +-------------------------- Item_8
LVL14 +---------------------------- ItemGroup_6
LVL15 +------------------------------ Item_9
LVL16 +-------------------------------- ItemGroup_7
LVL17 +---------------------------------- Item_10
LVL18 +------------------------------------ ItemGroup_8
LVL19 +-------------------------------------- Item_11
LVL20 +---------------------------------------- ItemGroup_9
LVL21 +------------------------------------------ Item_12
```
**Grubhub Menu**
```
LVL1 +-- Menu
LVL2 +---- Section
LVL3 +------ Item (for Item_1)
LVL4 +-------- Modifier_Prompt (for ItemGroup_1)
LVL5 +---------- Modifier (for Item_2)
LVL5 +---------- Modifier (for Item_3)
LVL6 +------------ Modifier_Prompt (for ItemGroup_2)
LVL7 +-------------- Modifier (for Item_4)
LVL7 +-------------- Modifier (for Item_5)
LVL8 +---------------- Modifier_Prompt (for ItemGroup_3)
LVL9 +------------------ Modifier (for Item_6)
LVL10 +-------------------- Modifier_Prompt (for ItemGroup_4)
LVL11 +---------------------- Modifier (for Item_7)
LVL12 +------------------------ Modifier_Prompt (for ItemGroup_5)
LVL13 +-------------------------- Modifier (for Item_8)
LVL14 +---------------------------- Modifier_Prompt (for ItemGroup_6)
LVL15 +------------------------------ Modifier (for Item_9)
LVL16 +-------------------------------- Modifier_Prompt (for ItemGroup_7)
LVL17 +---------------------------------- Modifier (for Item_10)
LVL18 +------------------------------------ Modifier_Prompt (for ItemGroup_8)
LVL19 +-------------------------------------- Modifier (for Item_11)
LVL20 +---------------------------------------- Modifier_Prompt (for ItemGroup_9)
LVL21 +------------------------------------------ Modifier (for Item_12)
```

### Menu Creation
- The items on a restaurant's menu are the core of its operations. 
- The POS integration will need to create their menu in the Grubhub system and sync.
- Grubhub currently maintains a one-to-one relationship between physical locations and menus.
- To create menu, we have to construct a normalized menu object with the entire qu menu.
- Each menu schedule (e.g. lunch, dinner, weekends) contains menu sections (appetizers, entrees), which contain the individual menu items that customers order.
- We can also specify multiple sizes, each with a different pricing scheme.
- Each menu item can have multiple required or optional modifiers each with multiple selections. 
- We can use both sizes and modifiers & can set the price of the modifier to be contingent on the size.
- We can add the same item to the different categories based on specific externalIds in the normalized menu.
- We can also attach preset tags to the item to indicate dietary or delivery restrictions, such as alcohol, gluten-free, or spicy items.

### Menu - Selection logic for modifier prompt
- Prompt quantity setting is decided by the selection rule in EI for the item_group.
- Modifier quantity setting is decided from item configuration in EI on the item level.
- Default selection model is determined on the basis of quantity settings of indidvidual modifiers (items for an item group)

```
Example - 
If there are three modifier for a prompt and have their individual quantity config as follows -
modifier 1 - min = 0, max = 1
modifier 2 - min = 1, max = 1
modifier 3 - min = 0, max = 0

So, the default selection - min = 1, max = 2

modifier 1 - min = 1, max = 4
modifier 2 - min = 1, max = 1
modifier 3 - min = 1, max = 1

So, the default selection - min = 3, max = 3

defaul section min and max should be in the range of Prompt quantity setting min and max.
```
### Prompts With Included Qty > 0
- For ItemGroups that have IncludedQty > 0, we create a corresponding modifier prompt for Grubhub that only contains free modifiers (price - 0).
- We set the selection setting for the above prompt based on the IncludedQty value, max selection is limited by IncludedQty.
- The above changes were required because Grubhub selection was breaking for ItemGroups with IncludedQty > 0 and modifiers with max allowed selection > 1.

### Size Prompts

- Size prompt contains the details about the types of portions/sizes for the item and size based prices.
- For multi-portioned items in the Qu menu, we create an additional modifier prompt for the item for item portion/size selection. 
- The portions for the item are mapped to Grubhub modifiers which are then used in the size prompt.
- This prompt has selection settings configured such that it is required for the user to select one option from the available modifiers.
- We combine the portion in the main item itself for single-portioned items, so we do not need to create a size modifier prompt for the only portion.


### Price Logic
- If Item has size_prompt defined then the price is based on their different size price. 
- Further, the price of the sized modifier for a sized item depends on the selected size of the parent item.

### Item - Menu Media
- The image to be displayed for the item in the menu is provided through menu media object for the item which takes the image url for downloading the image. 

### Menu Validation
When the menu conversion fails for some reason, the menu itself will not be pushed to Grubhub and the following will be performed.
 - Update the menu status to `Error` in the ProviderMenus collection.
 - Log the exception.
 - Send a error message to trigger and save.

### Menu Clipping
During menu transformation, all base items that are identified as having one or more of the following issues that could cause order failures are “clipped” from the menu:
 - An item with a path that exceeds 21 levels
 - An item with a hierarchy that includes 2 item groups in a row
 - An item with a hierarchy that contains a virtual group

 ### Prompt display settings
 - Radio button is visible only if default selection min and max is 1 and one default modifier is provided.

### Menu Process Synchronization
Grubhub will attempt to process a menu for 5 minutes. After that time, the menu job will be canceled and failed. If the first menu job is still pending and a second menu job is pushed before 5 minutes are up (retry), it will be rejected. Because of this, we are using a retry wait time of 5 minutes before retrying a menu if we have not received a Menu Status Update Notification.

### Menu Related Functionality
- [Custom Tags](custom_tag.md##Custom-Tag-Support)
- [Stockouts](stockouts.md##Stock-outs)
- [Menu Taxes](taxes.md##Taxes)

### Additional References:
 - [Sequence Diagram: Menu Mapping](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1lxHfGJ8kWrIs062HlSTgzQubUxEC3Iuo)
 - [Data Flow Diagram: Menu Process](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1kV5A1DU6LARDYzldmFFUH0NzH2B3URY9)

 [BACK](../README.md#menus-mapping)