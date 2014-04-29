function popover_placement(po, el) {
  var win_width = window.innerWidth;
  var el_right = $(el).offset().left + $(el).outerWidth(true);
  if ((win_width - el_right) < 280)
    return 'bottom';
  return 'right';
}
function popover_content() {
  var btn_close = '<button type="button" class="close" data-fld="#' +
                  $(this).attr('id') + '">&times;</button>';
  return btn_close + $(this).data('errors');
}
$(document).ready(function () {
  var popover_sets = {
    container: 'body',
    trigger: 'manual',
    placement: popover_placement,
    html: true,
    content: popover_content
  };
  var flds = $('[rel="popover"]');
  flds.popover(popover_sets);
  if (flds.length > 1) {
    flds.each(function (i) {
      $(this).on('show.bs.popover', function () {
        var popover = $(this).data('bs.popover').tip();
        popover.css('z-index', 1010 - i);
      });
    });
  }
  flds.popover('show');
  var alert = $('#non_field_alert');
  if (alert.length > 0) {
    alert.bind('closed.bs.alert', function () {
      if ($('.popover').length > 0) {
        var el_height = $(this).outerHeight(true);
        $('.popover').each(function () {
          var po_top = $(this).offset().top;
          $(this).offset({top: po_top - el_height});
        });
      }
    });
  }
});
$(document).click(function (e) {
  if ($(e.target).is('.popover .close'))
    $($(e.target).data('fld')).popover('destroy');
});
$(window).resize(function () {
  if ($('.popover').length > 0)
    $('[rel="popover"]').popover('show');
});
