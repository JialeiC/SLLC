
window.scroll(function () {
    if ($(".navbar").offset().top > 50) {$(".navbar-fixed-top").addClass("top-nav");
    }
    else {$(".navbar-fixed-top").removeClass("top-nav");}})



function add_question(){
    var title_question = $("#title_question").val().trim();

    var catalogs_question = $("#catalogs_question  option:selected").val();
    var content_question = $("#content_question").val().trim();
    if(title_question==""){
        alert("Please input title_question");
        return;
    }
    if(content_question==""){
        alert("Please input content_question");
        return;
    }
    $.ajax({
        url:"../../../rango/addquestion_do/",
        type:"POST",
        data:{ title_question:title_question, catalogs_question:catalogs_question, content_question:content_question},
        success:function(data){
                window.location.href = data
        },
        fail:function(data){
            alert("false")
        }
    })
}

