$(document).ready(function (){
	$('#menu').on('click', function(){
		$('.menu').toggleClass('mostrar');
	});
});

function cambiarTexto(){
	document.getElementById('fileText').innerHTML = "Foto seleccionada exitosamente";
}