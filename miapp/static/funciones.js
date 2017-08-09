$(document).ready(function(){
 // funciones para la plantilla "tema"
  $("#boton_tema").click(function(){
      $("#form_expe").hide();
      $("#form_tema").show();
  });
  $("#boton_expe").click(function(){
      $("#form_tema").hide();
      $("#form_expe").show();
  });
  // funciones para la plantilla "experimento"
  $("#boton_edit_expe").click(function(){
      $("#form_editar_expe").show();
      $("#contenido_expe").hide();
      $("#form_revision").hide();
      $("#btns-edit-expe").hide();
  });
  $("#boton_cancel_edit_expe").click(function(){
      $("#form_editar_expe").hide();
      $("#contenido_expe").show();
      $("#form_revision").show();
      $("#btns-edit-expe").show();
      $('body, html').animate({scrollTop: '0px'}, 300);
  });
});
