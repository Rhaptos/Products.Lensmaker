//Code that inserts a branding bar if the user viewed a lens and then navigated to a page in the lens.

//Note: This _is_ done on body.onload (causes screen flicker, but doesn't break IE 7 and 8).
Ext.onReady(function() {
    //Light-weight branding (LWB)
    var lenslinks = Ext.DomQuery.select('.lenslink');
    var pageLenses = []; //All the lensid's (taken from the <a> tags)

    for(var i=0; i < lenslinks.length; i++) {
      var href = lenslinks[i].getAttribute('href');
      //href is not absolute, so we don't need to convert the url to a path.
      pageLenses.push(href);
    }

    var rawCookie = readCookie('lenses');
    var cookieLenses = rawCookie ? rawCookie.split('|') : [];

    //Prune the cookie list with lenses this module is in and then
    //if at least 1 is left, display branding for the one on top of the stack.
    var candidateLens = null;
    for(var c=0; c < cookieLenses.length; c++) {
      var cLens = cookieLenses[c].split('#');
      for(var p=0; p < pageLenses.length; p++) {
        var pLens = pageLenses[p];
        //IE 6 converts all a href="/relative/path" links to be absolute
        // This is a problem, so instead of checking equality
        // (to see if this content is in a bannered lens)
        // we need to check if the lens path is CONTAINED in the href.
        //if(cLens[0] == pLens) {
        if(pLens.indexOf(cLens[0]) >= 0) {
          candidateLens = cLens;
        }
      }
    }

    if(candidateLens && candidateLens.length <= 6) {
      var lensPath = unescape(candidateLens[0]);
      var color = candidateLens[1];
      var fgColor = candidateLens[2];
      var title = unescape(candidateLens[3]);
      var hasLogo = ( candidateLens[4] == 'true' );
      var lensCategory = candidateLens[5];
      var portalTop = Ext.get('cnx_portal-top');
      if ( portalTop ) {
        //TODO: Use the lens url (endsWith) to know which message to use
        var bannerMessage = '';
        if ( lensCategory == 'Endorsement' ) {
            bannerMessage = 'Content endorsed by: ';
        }
        else if ( lensCategory == 'Affiliation' ) {
            bannerMessage = 'Content affiliated with: ';
        } else if ( lensCategory == 'List' ) {
            bannerMessage = 'Content included in lens: ';
        }

        var linkStyle = ''; //'text-decoration:none;';
        var bannerStyle = '';
        if ('' != color) {
          bannerStyle = 'background-color: #' + color + ';';
          bannerStyle += ' color:#'+fgColor+';';
          linkStyle += ' color:#'+fgColor+';';
        } else {
          bannerStyle = 'color:#ffffff;'; //for the message preceding the link
          linkStyle += ' color:#ffffff;';
        }
        Ext.DomHelper.append(portalTop,
           { tag:'div', id:'cnx_branding_banner', style:bannerStyle,
             children:[
               bannerMessage,
               { tag:'a', href:lensPath, style:linkStyle, children:[title]}
             ]
           }
        );
      }

      var leftPanelTop = Ext.get('cnx_sidebar_column');
      if ( hasLogo && leftPanelTop ) {
        Ext.DomHelper.insertBefore(leftPanelTop.first(),
          { tag:'div', id:'cnx_branding_logo',
            children:[
              { tag:'a', href:lensPath,
                children:[
                  { tag:'img', src:lensPath + "/logo", alt:title }
                ]
              }
            ]
          }
        );
      }
    }

}) ;//();

