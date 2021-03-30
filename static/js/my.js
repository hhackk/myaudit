$("#tree").fancytree({
  checkbox: true,
  selectMode: 3,

  source: {
    url: "searchkeys.json"
  },

  select: function(event, data) {
    console.log(data);
  }
});


function show_result_code_search() {
  var result_ids = [];
  $.ajax({
    url: `/api/result_ids`,
    async: false,
    success: function (data) {
      result_ids = data.result_ids
    }
});

var pagination_container=$('#pagination-results');
pagination_container.pagination({
  dataSource: result_ids,
  locator: 'result_ids',
  pageSize: 1,
  autoHidePrevious: true,
  autoHideNext: true,
  callback: function (response, pagination) {
      ids = response.join(',')
      $.ajax({
          url: `/api/resultsbyids?ids=${ids}`,
          async: false,
          success: function (data) {
              //event.preventDefault();
              var result_code_search_script = $("#result-code-search-template").html();
              var result_code_search_tmpl = Handlebars.compile(result_code_search_script);
              var results_context = {
                searchResults: data
            };              
              var result_code_search_html = result_code_search_tmpl(results_context);
              $('.result-code-search').html(result_code_search_html);              
          }
      });
    }
  })

  
}

show_result_code_search();


$('.list-group-item').on('click', function() {
  var $this = $(this);
  var $alias = $this.data('alias');
  $('.active').removeClass('active');
  $this.toggleClass('active');
  console.log($this);
})

const firstIndex = $(this).find('.list-group-item').first().index();
const lastIndex = $(this).find('.list-group-item').last().index();
$('.list-group').bind('keydown', function(e){
  var index = $(this).find('.active').index();  
  switch(e.which){
    case 38:
      index = (index == firstIndex ? lastIndex : index - 1);
      break;
    case 40:
      index = (index == lastIndex ? 0 : index + 1);
      break;
  }  
  $(this).find('.active').removeClass('active');
  $(this).find('.list-group-item:eq( '+ index +' )').addClass('active');
  
});