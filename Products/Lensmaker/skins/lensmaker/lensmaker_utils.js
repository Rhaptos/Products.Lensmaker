function selectCheckboxes(el, show){
  /* Recursively select and display any checkboxes found inside el */
  if(el.tagName && el.type &&
     (el.tagName.toLowerCase()=='input') &&
     (el.type.toLowerCase()=='checkbox')){
    if(show){
      el.checked=true;
      el.style.display='inline';
    } else {
      el.checked=false;
      el.style.display='none';
    }
  }
  for(var i = 0; i<el.childNodes.length; i++){
    selectCheckboxes(el.childNodes[i], show);
  }
}

function onApprove(el){
  /* When a checkbox is selected on the review/approve view, make the nested
   * per-lens checkboxes visible and select them. When the checkbox is
   * deselected, make them invisible and hide them. */
  holder = document.getElementById('metadata_'+el.value);
  selectCheckboxes(holder, el.checked);
}
