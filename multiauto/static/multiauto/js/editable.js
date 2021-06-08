
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
        var validation = /^[a-zA-Z_\.\-0-9]+@[a-zA-Z_\-0-9]+(\.[a-zA-Z_\-0-9]+)*$/
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
        var url = element.attr("url");
        var func = element.attr("function");
        function end(options) {
            options = [{key:"None",value:"selecione um..."}].concat(options)
            var tag = "<select type='text'>";
            for (var i = 0; i < options.length; i++) {
                tag += "<option value='" + options[i].key + "' "+ (options[i].key == valorOriginal?"selected":"") +">" + options[i].value + "</option>"
            }
            tag += "</select><button type='button'>OK</button>"
            element.html(tag);
            element.find('button').first().on("click",function(event){
                var type = $($(this).parent()).attr("type")
                gettypeEdiTable(type).onclose($($(this).parent()).children().first())
            })
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
        if(value == "None"){
            element.parent().attr("value", "").text("");
        }else{
            element.parent().attr("value", value).text(novoConteudo);
        }
    }
    typeEdiTable.push(type)

    type = {}
    type.name = "multiauto"
    type.onedit = (element) => {
        var conteudoOriginal = element.text();
        var idOriginal = element.attr('value')||"";


        var options = element.attr("options");
        var url = element.attr("url");
        var func = element.attr("function");
        function end(options) {
            element.html("<input type='text' value='" + conteudoOriginal + "'/><input type='hidden' value='"+idOriginal+"'/>");
            multiauto(element.children().first(),element.children().last(), options);
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
        var options = element.parent().attr("options");
        var func = element.parent().attr("function");
        if (options) {
            regex = /\((?<key>\w+),(?<value>[^\)]+)\);/gm;
            reg = /\((?<key>\w+),(?<value>[^\)]+)\);/;
            options = options.match(regex)
            options = options.map((d) => d.match(reg).groups)
        } else if (func) {
            func = func.split("\(")
            attr = func[1].slice(0, func[1].length - 1).split(",")
            func = func[0]
            options = window[func](...attr)
        }else{
            options = []
        }
        var novoConteudo = element.val();
        var novoid = multiauto_data(multiauto_split(novoConteudo),options);
        element.parent().attr("value", novoid);
        element.parent().text(novoConteudo);
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
        var name = $(list[i]).attr('name')
        if (name == col) {
            return i
        }
    }
}
function relatedEdiTable(table, col) {
    table = table ? table + " " : ""
    col = columnEdiTable(table, col)
    var list = $(table + "tr")
    var ret = []
    for (var i = 1; i < list.length; i++) {
        var r = {key:$(list[i]).attr('pk'),value:$($(list[i]).find("td")[col]).html()}
        if (!r.key){
            r.key = "$"+i
        }
        ret.push(r)
    }
    return ret
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
function delrowEdiTable(table) {
    table = table ? table + " " : ""
    $(table + "tbody").find('tr').last().remove()
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
        var edicao = $(this).find("td.celulaEmEdicao")
        for (var i=0;i<edicao.length;i++){
            var type = $(edicao[i]).attr("type")
            gettypeEdiTable(type).onclose($(edicao[i]).children().first())
        }

        var values = []
        var heads = ['pk']
        values.push([])
        th = $(this).find(table + " thead th")
        for (var i = 0; i < th.length; i++) {
            values.push([])
            heads.push($(th[i]).attr("name"))
        }

        var rows = $(this).find(table + " tbody tr")
        for (var i = 0; i < rows.length; i++){
            values[0].push($(rows[i]).attr('pk'))
            var tags = $(rows[i]).find("td")
            for (var j = 1; j < heads.length; j++) {
                var tag = $(tags[j-1])
                if (tag.attr("value"))
                    values[j].push(tag.attr("value"))
                else
                    values[j].push(tag.html())
            }
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
