$(function() {


	$('.d-flex [href]').each(function (){
		if (this.href == window.location.href) {

			if ($(this).hasClass("text-black") == false){
				$(this).addClass('text-white');
			}
		}
	});

	$('#select').change(function() {
		$('.income').hide();
		$('#' + $(this).val()).show();
	});

	//кнопка на аналитике
	$('.row [href]').each(function (){
		if (this.href == window.location.href) {
			if ($(this).hasClass("active-button") == false){
				$(this).addClass('active-button');
				$("#bt1").removeClass('active-button')
			}
		}
	});


	$("#btn1").click( function () {
		let n1 = $("input[name=sum]").val() * 1;
		let n2 = $("input[name=rate]").val() * 1;
		let result = 'Некорректный ввод';
		let rate = $("select[name=statesel]").val();
		let state = $('#sel option:selected').text();
		let form = ($('#checkbox').is(':checked'));



		if ((state =='США') && (form == true) ) {
			let i = n1 * n2 * 0.03;
			result = Math.round(i);
		}
		else if(rate < 13) {
			tax = 13 - rate;
			let i = (tax / 100) * n1 * n2
			result = Math.round(i);
		}
		else {
			result = "У вас нет налога"
		}
		if(isNaN(n1) || isNaN(n2)) {
			result = 'Некорректный ввод'
		}
		$("input[name=result1]").val(result);
	});

	$("#btn2").click( function () {
		let n1 = $("input[name=pr2]").val() * 1;
		let n2 = $("input[name=kpr2]").val() * 1;
		let n3 = $("input[name=po2]").val() * 1;
		let n4 = $("input[name=kpo2]").val() * 1;
		let result;

		let i = (n1 - n2 - n3 - n4) * 0.13;
		result = Math.round(i);

		if(isNaN(result)) {
			result = 'Некорректный ввод'
		}
		$("input[name=result2]").val(result);
	});

	$("#btn3").click( function () {


		let n1 = $("input[name=pr3]").val() * 1;
		let n2 = $("input[name=kpr3]").val() * 1;
		let n3 = $("input[name=po3]").val() * 1;
		let n4 = $("input[name=kpo3]").val() * 1;
		let result;

		let i = (n1 - n2 - n3 - n4) * 0.13;
		result = Math.round(i);

		if(isNaN(result)) {
			result = 'Некорректный ввод'
		}
		$("input[name=result3]").val(result);
	});

});

