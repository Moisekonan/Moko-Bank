$(document).ready(function() {

    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000); // <-- time in milliseconds

    $('#afficherPwd').click(function(){
        var x = $("#pwdInput")
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    });

    $('.reset_btn').click(function(event){
        event.preventDefault();
        $("#client_ssn_id")[0].value = "";
        $("#nom")[0].value = "";
        $("#email")[0].value = "";
        $("#age")[0].value = "";
        $("#pays")[0].value = "";
        $("#ville")[0].value = "";
    });

    $('#client_ssn_id, #age, #id_client, #id_compte, #montant').keypress(function(event){
        if(event.which = 8 && isNaN(String.fromCharCode(event.which))){
            event.preventDefault(); //stop character from entering input
        }
    })

    $('#nom, #pays, #ville').keypress(function(event){
        if(!((event.charCode > 64 && event.charCode < 91) || (event.charCode > 96 && event.charCode < 123) || event.charCode==32)){
            event.preventDefault(); //stop character from entering input
        }
    })

    $('#voir_client').validate({
        rules: {
            id_client: {
                required: '#client_ssn_id:blank'
            },
            client_ssn_id: {
                required: '#id_client:blank'
            }
          }
    })

    $('#voir_cmpt').validate({
        rules: {
            id_client: {
                required: '#id_compte:blank'
            },
            id_compte: {
                required: '#id_client:blank'
            }
          }
    })

    $('select.sel_type').change(function () {
        if (this.value == 'Actuel')
            $('select.sel_type').not(this).val('Épargne');
        if (this.value == 'Épargne')
            $('select.sel_type').not(this).val('Actuel');
    });

    $('.actualiser_client').click(function(event){
        event.preventDefault()
        target = event.target
        id_client = parseInt(target.dataset.id_client)
        var data = {"id_client": id_client}
        $.ajax({
            type: "POST",
            url: "/api/v1/carnetclient",
            dataType: 'json',
            data: JSON.stringify(data),
            contentType:"application/json; charset=UTF-8"
        }).done(function(result){
            console.log(result)
            parrent_ele = target.parentElement.parentElement
            parrent_ele.children[2].innerHTML = result.message
            parrent_ele.children[3].innerHTML = result.date
        }).fail(function(error){
            console.log(error)
        })
    })

    $('.actualiser_compte').click(function(event){
        event.preventDefault()
        target = event.target
        id_compte = parseInt(target.dataset.id_compte)
        var data = {"id_compte": id_compte}
        $.ajax({
            type: "POST",
            url: "/api/v1/carnetcomptes",
            dataType: 'json',
            data: JSON.stringify(data),
            contentType:"application/json; charset=UTF-8"
        }).done(function(result){
            console.log(result)
            parrent_ele = target.parentElement.parentElement
            parrent_ele.children[3].innerHTML = result.statut
            parrent_ele.children[4].innerHTML = result.message
            parrent_ele.children[5].innerHTML = result.date
        }).fail(function(error){
            console.log(error)
        })
    })
});