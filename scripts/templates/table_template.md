# Summary Table

|Created|Title|Description|Author(s)|Query|
| :---| :---| :---| :---|:---|
{% for q in community|sort(attribute='creation_date') %}|{{q['creation_date']}} |{{q['title']}} |{{q['description']}} |{{q['author']}} |```{{q['query'] | replace('\n', ' ')}}```|
{% endfor %}