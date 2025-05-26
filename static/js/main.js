jQuery("button.upload").click(function(){
    jQuery("#first-popup").show("fast");
    jQuery("#first-popup .dialog").show();
})

jQuery("#first-popup #close").click(function(){
    jQuery("#first-popup").hide("fast");
})
jQuery("button.menu-icon").click(function(){
    jQuery("#main-header").addClass("animate");
    jQuery("#main-header").addClass("open");
})
jQuery("#main-header .menu-close-icon").click(function(){
    jQuery("#main-header").removeClass("open animate");
})