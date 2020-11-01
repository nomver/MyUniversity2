$(document).ready(function(){
	var ShowForm=function(){
		var btn=$(this);
		$.ajax({
			url:btn.attr('data-url'),
			type:'get',
			dataType:'json',
			beforeSend:function(){
				$('#modal-book').modal('show');
			},
			success: function(data){
				$('#modal-book .modal-content').html(data.form);
			},
		});

	};
	$('#book_form').click(ShowForm);

	var SaveForm=function(){
		var form=$(this);
		$.ajax({
			url:form.attr('data-url'),
			data:form.serialize(),
			type:form.attr('method'),
			dataType:'json',
			success:function(data){
				if(data.form_is_valid==true){
					$('#book-table tbody').html(data.book_list);
					$('#modal-book').modal('hide');
				}
				else{
					$('#modal-book .modal-content').html(data.form)
				}
			}

		});
		return false;
	};
	$('#modal-book').on('submit','.form',SaveForm);
	$('#book-table').on('click','#book_update',ShowForm);
	$('#book-table').on('click','#book_delete',ShowForm);
	$('#check').mouseleave(function(){
		var content=$(this).val();
		var contnt=$(this);
		$.ajax({
			url:'/if_exist',
			type:'get',
			success:function(data){
				console.log(data);
			}
		});
	});
});	