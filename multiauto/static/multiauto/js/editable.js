
var typeEdiTable = [];
(() => {//Configurando tipos
    genericonedit = (element) => {
        var conteudoOriginal = element.text();
        element.html("<input type='text' value='" + conteudoOriginal + "' />");
    }
    type = {}
    type.name = "text"
    type.onedit = genericonedit
    type.onclose = (element) => {
        var novoConteudo = element.val();
        element.parent().text(novoConteudo);
        element.parent().attr("value", novoConteudo);
    }
    typeEdiTable.push(type)

    type = {}
    type.name = "email"
    type.onedit = genericonedit
    type.onclose = (element) => {
        var novoConteudo = element.val();
        var validation = /^[a-zA-Z_\.\-0-9]+@[a-zA-Z_\-0-9]+(\.[a-zA-Z_\-0-9]+)?$/
        if (!novoConteudo || !novoConteudo.match(validation)) {
            element.parent().attr("style", "background-color:#f55")
        }
        element.parent().text(novoConteudo);
        element.parent().attr("value", novoConteudo);
    }
    typeEdiTable.push(type)

    type = {}
    type.name = "integer"
    type.onedit = genericonedit
    type.onclose = (element) => {
        var novoConteudo = element.val();
        var validation = /^-?[0-9]+$/
        if (!novoConteudo || !novoConteudo.match(validation)) {
            element.parent().attr("style", "background-color:#f55")
        }
        element.parent().text(novoConteudo);
        element.parent().attr("value", novoConteudo);
    }
    typeEdiTable.push(type)

    type = {}
    type.name = "number"
    type.onedit = genericonedit
    type.onclose = (element) => {
        var novoConteudo = element.val();
        var validation = /^-?(([0-9]+([\.,][0-9]*)?)|([\.,][0-9]+))$/
        if (!novoConteudo || !novoConteudo.match(validation)) {
            element.parent().attr("style", "background-color:#f55")
        }
        element.parent().text(novoConteudo);
        element.parent().attr("value", novoConteudo);
    }
    typeEdiTable.push(type)

    type = {}
    type.name = "select"
    type.onedit = (element) => {
        var valorOriginal = element.attr("value");

        var options = element.attr("options");
        var url = element.attr("options");
        var func = element.attr("function");
        function end(options) {
            var tag = "<select type='text' selected=" + valorOriginal + ">";
            for (var i = 0; i < options.length; i++) {
                tag += "<option value='" + options[i].key + "'>" + options[i].value + "</option>"
            }
            tag += "</select>"
            element.html(tag);
        }
        if (options) {
            regex = /\((?<key>\w+),(?<value>[^\)]+)\);/gm;
            reg = /\((?<key>\w+),(?<value>[^\)]+)\);/;
            options = options.match(regex)
            options = options.map((d) => d.match(reg).groups)
            end(options)
        } else if (url) {
            $.getJSON(url, function (data) {
                options = data;
                strop = options.map((d) => `(${d.key},${d.value});`).reduce((d, a) => d + a);
                element.attr("options", strop);
                end(options)
            });
        } else if (func) {
            func = func.split("\(")
            attr = func[1].slice(0, func[1].length - 1).split(",")
            func = func[0]
            options = window[func](...attr)
            end(options)
        }
    }
    type.onclose = (element) => {
        var value = element.children("option:selected").val();
        var novoConteudo = element.children("option:selected").html();
        element.parent().attr("value", value).text(novoConteudo);
    }
    typeEdiTable.push(type)

    type = {}
    type.name = "multiauto"
    type.onedit = (element) => {
        var conteudoOriginal = element.text();

        var options = element.attr("options");
        var url = element.attr("options");
        var func = element.attr("function");
        function end(options) {
            element.html("<input type='text' value='" + conteudoOriginal + "'/>");
            multiauto(element.children().first(), options);
        }
        if (options) {
            regex = /[^;]+;/gm;
            reg = /([^;]+);/;
            options = options.match(regex)
            options = options.map((d) => d.match(reg)[1])
            end(options)
        } else if (url) {
            $.getJSON(url, function (data) {
                options = data;
                strop = options.map((d) => `${d.value};`).reduce((d, a) => d + a);
                element.attr("options", strop);
                end(options)
            });
        } else if (func) {
            func = func.split("\(")
            attr = func[1].slice(0, func[1].length - 1).split(",")
            func = func[0]
            options = window[func](...attr)
            end(options)
        }
    }
    type.onclose = (element) => {
        var novoConteudo = element.val();
        element.parent().text(novoConteudo);
        element.parent().attr("value", novoConteudo);
    }
    typeEdiTable.push(type)
})()
function gettypeEdiTable(type) {
    for (var i = 1; type && i < typeEdiTable.length; i++) {
        if (type == typeEdiTable[i].name) {
            type = typeEdiTable[i]
        }
    }
    if (!type || typeof (type) == 'string') {
        type = typeEdiTable[0]
    }
    return type
}

function set_eventEdiTable() {
    $("td.editable").dblclick(function () {
        var conteudoOriginal = $(this).text();
        var value = $(this).attr('value');
        var type = $(this).attr("type")

        $(this).addClass("celulaEmEdicao");
        //$(this).html("<input type='text' value='" + conteudoOriginal + "' />");
        gettypeEdiTable(type).onedit($(this))
        $(this).children().first().focus();

        $(this).children().first().keypress(function (e) {
            if (e.which == 13) {
                gettypeEdiTable(type).onclose($(this))
                $(this).parent().removeClass("celulaEmEdicao");
            }
            if (e.key === "'") {// TODO ajeitar pra escape
                $(this).parent().text(conteudoOriginal);
                $(this).parent().attr("value", value);
                $(this).parent().attr("type", type);
                $(this).parent().removeClass("celulaEmEdicao");
            }
        });

        $(this).children().first().blur(function () {
            gettypeEdiTable(type).onclose($(this))
            $(this).parent().removeClass("celulaEmEdicao");
        });
    });
};

function columnEdiTable(table, col) {
    table = table ? table + " " : ""
    list = $(table + "th")
    for (var i = 0; i < list.length; i++) {
        if ($(list[i]).attr('name') == col) {
            return i
        }
    }
}
function getvaluesEdiTable(table, col) {
    table = table ? table + " " : ""
    col = columnEdiTable(table, col)
    list = $(table + "tr")
    ret = []
    for (var i = 1; i < list.length; i++) {
        console.log($(list[i]).find("td"))
        ret.push($($(list[i]).find("td")[col]).html())
    }


    return ret
}
function convert_selectEdiTable(values) {
    return values.map((d, i) => { return { key: i, value: d } }).filter((d) => d.value)
}
function relatedEdiTable(table, col) {
    return getvaluesEdiTable(table, col).filter((d) => d)
}
function related_selectEdiTable(table, col) {
    return convert_selectEdiTable(relatedEdiTable(table, col))
}

function addrowEdiTable(table, row) {
    table = table ? table + " " : ""
    tr = ""
    if (!row) {
        list = $(table + "thead th")
        tr += "<tr><td type='text' class='editable'>...editar...</td>"
        for (var i = 1; i < list.length; i++) {
            tr += "<td type='text' class='editable'></td>"
        }
        tr += "</tr>";
    } else
        tr = row
    $(table + "tbody").append(tr)
    set_eventEdiTable()
}
function setEdiTable(table) {
    table = table || "table"
    $(() => set_eventEdiTable(table))
    parent = $(table).parent()

    while (parent[0].tagName != "FORM") {
        parent = $(parent[0]).parent()
        if (parent[0].tagName != "BODY")
            return
    }
    $(parent[0]).submit(function (event) {
        var values = []
        var heads = []
        th = $(this).find(table + " thead th")
        for (var i = 0; i < th.length; i++) {
            values.push([])
            heads.push($(th[i]).attr("name"))
        }

        var rows = $(this).find(table + " tbody tr")
        for (var i = 0; i < rows.length; i++)
            for (var j = 0; j < heads.length; j++) {
                tag = $($(rows[i]).find("td")[j])
                if (tag.attr("value"))
                    values[j].push(tag.attr("value"))
                else
                    values[j].push(tag.html())
            }

        for (var i=0;i<heads.length;i++) {
            var input = $("<input>")
                .attr("type", "hidden")
                .attr("name", heads[i]).val(values[i].join(" # "));
            $(this).append(input);
        }


        return true
    })
}
