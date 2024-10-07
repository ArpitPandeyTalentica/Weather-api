[BACK](../README.md#menus-mapping)

## Custom Tag Support
- Tags for menu items are used to flag certain items for special delivery handling, and regulatory treatment based on the tag ID applied in the platform setting.
- To denote that an item is eligible for certain flags and icons on Grubhub diner properties.

### Alcohol Tagging
- The restaurant’s integration partner needs to support the ability to send alcoholic items to Grubhub with a tag indicating that the item contains alcohol. 
- Alcohol will only be included at the ITEM level and not with the modifiers. 
- The restaurant itself must complete the required Grubhub compliance, otherwise, the alcohol items will be automatically hidden from their menu.

### Model Structure
- This will be added as an array of Tags property within the item and modifier of NormalizedMenu.
```
{
  "group": <string>,
  "name": <string>
}

group - Tag group - Currently the only valid group is "LEGACY"
name - Grubhub based tag name enum like - "ALCOHOL", GLUTEN_FREE, "SPICY" etc
```

### Approach
- Firstly, we create a lookup of TagId with QuTagName as per the dietary platform setting.
- Dietary platform settings that allow the user to specify a tag ID that maps to a specific type of tag.
```
Dictionary<TagId,QuTagName> QuTagTypeLookups

TagId : <int> - TagId mentioned in dietary platform setting for respective tag
QuTagName : <string> - Specify a tag ID that map to specific type of tag

Example - {1,Alcohol}, {2,GlutenFree} etc
```
- Then we create another lookup of QuTagName with a Grubhub-based tag name.
```
Dictionary<QuTagName, GrubhubTagName> GrubhubTagTypeLookups

GrubhubTagName - Grubhub based tag name

Example - {Alcohol, ALCOHOL}, {GlutenFree, GLUTEN_FREE} etc
```
- Item's dietary IDs are tagged with the respective Grubhub tag name.
- Then We sync the menu to Grubhub and then tags are reflected on the item.
- Currently `GLUTEN_FREE`, `NUT_FREE`, `VEGAN` etc don’t have tags on the item like the spicy tag.
- They will cause the restaurant to show up when someone searches `Gluten Free`, etc, in the search bar. 

### Example
1. If any item's nutritionInfo have some dietaryId defined - dietaryIds - {1,2}
   We checked in QuTagTypeLookups for an item's dietaryIds and accordingly tagged the name from GrubhubTagTypeLookups.
   
2. So, final Tags created as - 
```
"tags": [
          {
           "group": "LEGACY",
            "name": "ALCOHOL"
          },
          {
           "group": "LEGACY",
            "name": "GLUTEN_FREE"
          },
        ],
```
 
### Additional References:
 - [Sequence Diagram: Custom Tag](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#G1d-T63cUdnHL81XmZQM_OVAsAx2VI1OVd)
 - [Documentation:](https://developer.grubhub.com/docs/8xfKCX3PhOoULbHqn7HWq/alcohol)

 [BACK](../README.md#menus-mapping)