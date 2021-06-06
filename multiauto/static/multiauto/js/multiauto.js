function multiauto_split(val) {
    return val.split(/,\s*/);
}
function extractLast(term) {
    return multiauto_split(term).pop();
}

function multiauto_data(terms, tags) {
    return terms.map(term => {
        for (var i = 0; i < tags.length; i++) {
            if (term == tags[i].value) {
                return "" + tags[i].key
            }
        }
        return ""
    }).join(", ");
}

function multiauto_onsubmit(event){
    console.log(this)
}

function multiauto(tag_value, tag, availableTags) {
    var values = availableTags.map(a => a.value)
    tag_value// don't navigate away from the field on tab when selecting an item
        .on("keydown", function (event) {
            if (event.keyCode === $.ui.keyCode.TAB &&
                $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
        })
        .on("blur", function (event) {
            tag.val(multiauto_data(multiauto_split($(this).val()), availableTags))
        })
        .autocomplete({
            minLength: 0,
            source: function (request, response) {
                // delegate back to autocomplete, but extract the last term
                response($.ui.autocomplete.filter(
                    values, extractLast(request.term)));
            },
            focus: function () {
                // prevent value inserted on focus
                return false;
            },
            select: function (event, ui) {
                var terms = multiauto_split(this.value);

                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(", ");
                return false;
            }
        });
        tag.val(multiauto_data(multiauto_split(tag_value.val()), availableTags))
}