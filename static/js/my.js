$(function(){
    $(".helptext").css('display', 'none');
    $("#myText").css('display', 'none');
});

function toggle(cpid)
{
	var x = document.getElementById(cpid).style.display;
	if (x == 'none')
	{
		document.getElementById(cpid).style.display = 'block';
	}
	else
	{
		document.getElementById(cpid).style.display = 'none';
	}
}


function comment(taid, cmtid)
{
	var cmtext = document.getElementById(taid).value;
	
	$.ajax({
		type:"POST",
		url:"/comment_cmnt/"+cmtid,
		data: {
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
			'comment_text': cmtext,
			'post_id':document.getElementById("myText").value
		},
		success:function(orders)
        {
            $("#ajaxcmnt").html(orders);

        },
        error: function (jqXHR, textStatus, errorThrown)
             {
                 alert("Please login!");
             }
	});
}