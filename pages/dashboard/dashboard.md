# **Sales**{: .color-primary} Dashboard

<|{selected_location}|selector|lov={selector_location}|on_change=on_change_location|dropdown|label=Location|>

<br/>

<|layout|columns=1 1 1|gap=50px|
<|card|
**Sales**{: .color-primary}
<|{data_location.iloc[-1]['Location']}|text|class_name=h2|>
|>

<br/>
<br/>
<|layout|columns=1 1 1|gap=50px|
<|card|
**Sales**{: .color-primary}
<|{data_location.iloc[-1]['Units']}|text|class_name=h2|>
|>