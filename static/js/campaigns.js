$(document).ready(function () {
    $.getJSON("../ads/api/campaigns?account_id=" + account_id,
    function (json) {
        var tr;
        for (var i = 0; i < json["campaigns"].length; i++) {
            tr = $('<tr/>');
            var campaign_id = json["campaigns"][i].id
            tr.append("<td><a href='line_items?account_id=" + json["account_id"] + "&campaign_id=" + campaign_id + "'>" + json["campaigns"][i].name + "</a></td>");
            tr.append("<td>" + campaign_id + "</td>");
            $('.table').append(tr);
        }
    });

    $("#createCampaign").click(function(event){
      console.log("create Campaign");
      createCampaign(account_id, $("#campaign_name").val(), $("#campaign_daily_budget").val());
    });

});

// create new campaign
function createCampaign(account_id, campaign, daily_budget){
  $.getJSON("../../ads/api/campaign/new?account_id=" + account_id + "&campaign=" + campaign + "&daily_budget=" + daily_budget,
  function (json) {
    if (json['valid'] == true){
      location.reload();
    } else {
      console.log("error with queries");
      $('#campaignModal').modal('hide');
      $('.error').show();
      $('.error-msg').text("Error: " + json['response'][0]['message']);
    }

  });
}
