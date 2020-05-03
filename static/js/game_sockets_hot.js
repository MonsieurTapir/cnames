function reveal(word,team){
    var word_id=".card-panel#"+word;
    $(word_id).removeClass("grey lighten-2 hoverable gamecard")
    var to_add=""
    if(team=="red"){
        to_add="card-red darken-1";
    } else if (team=="blue"){
        to_add="card-blue darken-1";
    } else if (team=="grey"){
        to_add="grey darken-1";
    }else{
	to_add="black";
    }
    $(word_id).addClass(to_add);
    $(word_id+" > p").addClass("white-text");
}

$(document).ready(function() {
    $(".modal").modal();
    var room=window.location.pathname.substring(1);
    namespace = '/game';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('reveal',function(message) {
	var word=message['word'];
	var team=message['team'];
	var toast=message['toast'];
	console.log("revealing "+word)
	reveal(word,team);
	if(spy){
	    $("#"+word).addClass("guessed");
	}
	message="<b>"+word+"&nbsp</b>";
	if(team=="red" || team=="blue")
	{
	    message+="belonged to the<b>&nbsp"+team+"&nbsp</b>team";
	}
	else if(team=="grey")
	{
	    message+="was a<b>&nbsp"+team+"&nbsp</b>word";
	}
	else
	{
	    message+="was the black word";
	}
	if(toast){
	    Materialize.toast(message,3000);
	}
    });
    socket.on('connection_ack',function(){
	console.log("Connection established");
	console.log(room);
	console.log("asking to join channel "+room)
	socket.emit('join',{'room':room});
    });

    socket.on('update_score',function(message){
	var blue_score=message['blue_score'];
	var red_score=message['red_score'];
	$('#red_score').html(red_score);
	$('#blue_score').html(blue_score);
    });
    socket.on('end_game',function(message){
	team=message['winner'];
	if(team!="black")
	    Materialize.toast("<b>"+team+"&nbsp</b>team won !");
	else
	    Materialize.toast("the black word was guessed :(")
    });
    $('#modal_validation').modal({
	dismissible: true, // Modal can be dismissed by clicking outside of the modal
	opacity: .5, // Opacity of modal background
	inDuration: 300, // Transition in duration
	outDuration: 200, // Transition out duration
	startingTop: '4%', // Starting top style attribute
	endingTop: '10%', // Ending top style attribute
	complete: function() {$('.guess').remove(); } // Callback for Modal close	
    });

    $(this).on('click',".validate-word",function(){
	socket.emit('guess',{'word': this.id, 'room': room,'hot':"hot"});
    });
    $(this).on('click','.gamecard',function(){
	$('#word-validation').append("<h5 class='guess header teal-text'>"+this.id+"</h5>");
	$('.validate-word').attr('id',this.id);
	$('#modal_validation').modal('open');
    });

});
