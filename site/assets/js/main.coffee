$ = jQuery

pjaxContainer = '#main'

$.ajax
    url:'/assets/chosen.json'
    dataType: 'json'
  .done (data) ->
    html = ['<select id="search">']
    for page in data
      html.push "<option value='#{page.path}'>#{page.title}</option>"
    html.push '</select>'
    html = html.join('')

    $('#header').append $ html
    $('#search')
      .chosen()
      .change ->
        $.pjax
          url: this.value
          container: pjaxContainer
          fragment: pjaxContainer
          timeout: 2000

    $('body').on 'keypress', (event) ->
      if event.which is 47 # '/'
        event.preventDefault()
        $('#search_chzn').mousedown()

$('#main a[href^="/"]').pjax pjaxContainer,
  fragment: pjaxContainer
  timeout: 2000
