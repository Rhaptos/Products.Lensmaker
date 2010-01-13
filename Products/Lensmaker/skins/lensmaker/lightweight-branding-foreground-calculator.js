/* The following functions are used to set the foreground color */
function HexToRGB(hex) {
  var hex = parseInt(((hex.indexOf('#') > -1) ? hex.substring(1) : hex), 16);
  return {r: hex >> 16, g: (hex & 0x00FF00) >> 8, b: (hex & 0x0000FF)};
} 

function findBrightnessDif(rgb1, rgb2) {
  var brightness1 = ((rgb1.r * 299) + (rgb1.g * 587) + (rgb1.b * 114)) / 1000;
  var brightness2 = ((rgb2.r * 299) + (rgb2.g * 587) + (rgb2.b * 114)) / 1000;
  return Math.abs( brightness1 - brightness2 );
}

function findBestTextColor(brandColor) {
  if ( brandColor != null && brandColor.length == 0 ) {
    return '';
  }
  var bestTextColor = "ffffff";
  if (findBrightnessDif(HexToRGB(brandColor), HexToRGB('000000')) > findBrightnessDif(HexToRGB(brandColor), HexToRGB('ffffff')) ) {
    bestTextColor = "000000";
  }
  return bestTextColor;
}
