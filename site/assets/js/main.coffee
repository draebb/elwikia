$ = jQuery

$.ajax
    url:'/assets/chosen.json'
    async: false
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
        window.location.pathname = this.value

    $('body').on 'keypress', (event) ->
      if event.which is 47 # '/'
        event.preventDefault()
        $('#search_chzn').mousedown()
