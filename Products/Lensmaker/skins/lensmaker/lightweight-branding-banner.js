//Code that inserts a branding bar if the user viewed a lens and then navigated to a page in the lens.

//Note: This _is_ done on body.onload (causes screen flicker, but doesn't break IE 7 and 8).
$(document).ready(function() {
    //Light-weight branding (LWB)
    var rawCookie = readCookie('lenses').replace(/"/g,'');
    var cookieLenses = rawCookie ? rawCookie.split('|').reverse() : [];
    var brander = null;
    $('.cnx_branding_banner a').each(function(i,banner){
      var href = banner.getAttribute('href');
      if (cookieLenses.indexOf(href) != -1)
        brander = banner;
    });

if (brander){
    $(brander).parent().show();
    var href = brander.getAttribute('href');
    $(".cnx_branding_logo a[href='"+href+"']").parent().show();
    };
    
}) ;

