function choicebox(el) {
  return el.parent('.choicebox');
}
function toggle_choicebox(sel, opts) {
  opts.slideToggle();
  sel.toggleClass('options-show');
  sel.focus();
}
$('.choicebox button').click(function () {
  var sel = $(this);
  var box = choicebox(sel);
  var opts = box.find('ul');
  toggle_choicebox(sel, opts);
});
$('.choicebox li').click(function () {
  var opt = $(this);
  var opts = opt.parent('ul');
  var box = choicebox(opts);
  var tr = box.find('input');
  var val = tr.val();
  tr.val(opt.data('val'));
  opt.data('val', val);
  opt.attr('data-val', val);
  var sel = box.find('button');
  var sel_txt = sel.find('.txt');
  var txt = sel_txt.text();
  sel_txt.text(opt.text());
  opt.text(txt);
  toggle_choicebox(sel, opts);
});
$('.choicebox button').focus(function () {
  choicebox($(this)).addClass('on-focus');
}).blur(function () {
  choicebox($(this)).removeClass('on-focus');
});
