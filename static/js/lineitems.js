$(document).ready(function () {
  $.getJSON("../ads/api/line_items?account_id=" + account_id + "&campaign_id=" + campaign_id,
  function (json) {
      var tr;
      for (var i = 0; i < json["line_items"].length; i++) {
          tr = $('<tr/>');
          var item = json["line_items"][i]
          var line_item_id = item.id
          tr.append("<td><a href='line_items?account_id=" + json["account_id"] + "&campaign_id=" + json["campaign_id"]  + "'>" + item.name + "</a></td>");
          tr.append("<td>" + item.objective +"</td>")
          tr.append("<td>" + item.bid_amount +"</td>")
          tr.append("<td>" + item.id + "</td>");
          $('.table').append(tr);
      }
  });

  $("#createLineItem").click(function(event){
    console.log("create Campaign");
    createLineItem(account_id, campaign_id, $("#line_item_name").val(), $("#line_item_bid").val());
  });
});


// create new campaign
function createLineItem(account_id, campaign_id, name, bid){
  $.getJSON("../../ads/api/line_item/new?account_id=" + account_id
                                                      + "&campaign_id=" + campaign_id
                                                      + "&name=" + name
                                                      + "&bid_amount=" + bid,
  function (json) {
    if (json['valid'] == true){
      location.reload();
    } else {
      console.log("error with queries");
      $('#lineitemModal').modal('hide');
      $('.error').show();
      $('.error-msg').text("Error: " + json['response'][0]['message']);
    }

  });
}
