# Schematic pipeline methodology

---

## Overview

As seen in the [desktop user manual](https://github.com/datacentral-creator/Datacentral/blob/main/Desktop_user_manual.md) the schematics pipeline is a part of the projects add on of DataCentral. It's aim is to extend datacentral to include symbolic manipulation faculties. My [research into the effect of recommendation algorithms on the formation of culture](../Research_and_philosophy/algorithms.md) and later [memetic analysis of these findings](../Research_and_philosophy/Ontology.md) and [historical analysis](../Research_and_philosophy/Historical_context.md) revealed that there is strong evidence to suggest that the recommendation algorithm of YouTube has a structural bias towards the platform dictating the users behavioural patterns as opposed to the other way around. It would stand to reason that this pattern would also be found in other platforms powered by recommendation algorithms however this has not been shown empirically. The historical analysis revealed that this accelerates the historical pattern of symbols becoming increasingly abstract over time however in a historical context it is thought that this created a psychological demand for abstract reasoning pushing early humans from thinking in terms of mythology to thinking in terms of philosophy however in a contemporary context this demand falls onto the recommendation algorithm which could have adverse effects on users moving into the future. Because of this, the schematic pipeline maximises user intentionality in order to reverse this process. 

---

## 1. Link quantification
The first step of the schematic pipeline is for the user to select a link (recurring motif in the text file) that they want to investigate. This link then appears in the side panel along with how many times this link appears in the text(this can be how many times the link appears in the text file or how many times the link appears in a section of the text that the user has selected).

## 2. Link conversion
The link is then converted into database entries using a set of conversions defined by the user. An example of this is that the link "Beefburger" might be converted into "Bread" x 2 and "Beef" x 1. 

## 3. Schematic check and database retrieval
The program then retrieves a set of parameters defined by the user called a "schematic". The program then retrieves the values these database entries (such as "Bread" and "Beef") represent (such as nutritional information) and filter this data based on the parameters defined by the schematic. This will usually be some kind of quantity. The program then multiplies these quantities by how many times the database entry occurs in the conversion for example if "Beefburger" represents "Bread" x 2 and the quantity selected by the schematic is carbs (5000) then the carbs will be multiplied by 2. Finally the program multiplies this quantity by how many times the link appears in the text. This produces a final set of parameters which are displayed in the side panel along with the link and number of ocurrences. You can also choose to save this information to a file along with the current date and time or another date and time of your choosing. This then enters a system where you can query the data in this file over time, for example producing a graph of a specific parameter or predicting the likelihood of correlation between multiple parameters.

---

## Future scope

The next steps for the schematic pipeline would be for the program to be able to generate the database from the link and the parameters defined in the schematic automatically.
