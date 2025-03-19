
function findPokemon1(){
  findPokemon($("#Pokemon1Name").val(), "#Pokemon1Card")
}

function findPokemon2(){
  findPokemon($("#Pokemon2Name").val(), "#Pokemon2Card")

}

function findPokemon(name, cardId){
  $(cardId).html("<div class='loader w3-center'></div>")
  encoded_name = encodeURIComponent(name)
  $.ajax({
    url: `/api/v1/pokemon/${name}`,
    type: "GET",
    success: function(data){
      $(cardId).html(data)
    },
    error: function(jqXHR, textStatus, errorThrown){
      console.log(`error getting detail for Pokemon ${name} status: ${textStatus} error: ${errorThrown}`)
      $(cardId).html(jqXHR.responseText)
    }
  })
}

function startBattle(){
  pokemon1 = $("#Pokemon1Name").val()
  pokemon2 = $("#Pokemon2Name").val()
  $("#startBattleButton").disabled = true
  $.ajax({
    url: "/api/v1/battle",
    type: "POST",
    data: JSON.stringify({pokemon1: pokemon1, pokemon2: pokemon2}),
    success: function(data){
      $("#battleLog").html(data)
    },
    error: function(){
      console.log("Error starting battle")
      $("#battleLog").html("something went wrong, pls try again")
    },
    finally: function(){
      $("#startBattleButton").disabled = false
    }
  })
}