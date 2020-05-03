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

function hide_for_spy(){
    $('#hint-word-side').hide();
    $('#guesses-side').hide();
}
$(document).ready(function() {
    $(".modal").modal();
    
    var room=window.location.pathname.substring(1);
    namespace = '/game';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    if(spy_turn){
	hide_for_spy();
    }
    if(!my_turn || spy!="True" || (spy=="True" && !spy_turn) ){
	$('#spy_form').hide();
    }
    socket.on('connect', function() {
	socket.emit('my_event', {data: 'I\'m connected!'});
    });
    socket.on('reveal',function(message) {
	var word=message['word'];
	var team=message['team'];
	var toast=message['toast'];
	console.log("revealing "+word)
	reveal(word,team);
	if(spy=="True"){
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
    socket.on('room_ack',function(message){
	console.log("Joined room : "+ message['data']);
    });
    socket.on('update_score',function(message){
	var blue_score=message['blue_score'];
	var red_score=message['red_score'];
	$('#red_score').html(red_score);
	$('#blue_score').html(blue_score);
    });
    socket.on('update_turn',function(message){
	var team_turn=message['team_turn'];
	console.log(team_turn);
	console.log(my_team);
	if(team_turn==my_team){
	    my_turn=true;
	}else{
	    my_turn=false;
	}
	spy_turn=(team_turn.indexOf("spy")!==-1);
	if(team_turn==(my_team+"_spy") && spy=="True"){
	    $('#spy_form').show();
	}
	else{
	    $('#spy_form').hide();
	}
	if(team_turn.indexOf("spy")!==-1)
	{
	    $('#team-turn-side').html(team_turn.split("_")[0]);
	    $('#team-side-content').html("spy to hint");
	    $('#hint-word-side').hide();
	    $('#guesses-side').hide();
	}
	else
	{
	    var temp="blue";
	    if(team_turn.indexOf("red")!==-1)
	    {
		temp="red";
	    }
	    $('#team-turn-side').html(temp);
	    $('#team-side-content').html("team to guess");
	    $('#hint-word-side').show();
	    $('#guesses-side').show();
	}
    });
    socket.on('wtf',function(message){
	console.log(message['data']);
    });
    socket.on('update_guesses',function(message){
	$('#guesses-side > b').html(message['guesses']);
    });
    socket.on('receive_hint',function(message){
	$('#hint-word-side > b').html(message['hint_word']);
	$('#guesses-side > b').html(message['guesses']);
	Materialize.toast("Guess &nbsp<b>"+message['hint_word']+"</b>&nbsp in &nbsp "+message['guesses'],3000)
    });
    socket.on('player_join',function(message){
	console.log("new player "+message['username']+" in team "+message['team']);
	var team=message['team'];
	var username=message['username'];
	var color=(team=="red")?"card-red":"card-blue";
	if($("#player-"+username).length==0){
	    $("#"+team+"_team").append("<li> <a class='"+color+"-text name' id='player-"+username+"'>"+ username +"</a></li>");
	    Materialize.toast(username+" joined &nbsp;<span class='"+color+"-text text-lighten-2'>"+team+"</span>&nbsp team !", 3000);
	}
    });
    socket.on('player_left',function(message){
	var username=message['username'];
	
	console.log("player left "+username)
	var sel=$("#player-"+username);
	if(sel.length!=0){
	    sel.remove();
	    Materialize.toast(username+" left the game !", 3000);
	}
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
    $(this).on('click',".gamecard",function(){
	if(my_turn && !spy_turn){
	    $('#word-validation').append("<h5 class='guess header teal-text'>"+this.id+"</h5>");
	    $('.validate-word').attr('id',this.id);
	    $('#modal_validation').modal('open');
	}
    });
    $(this).on('click',".validate-word",function(){
	socket.emit('guess',{'word': this.id, 'room': room,'hot':"False"});
    });

    $("#submit-hint").click(function(){
	var hint_word=$('#hint-word').val();
	var guesses=$('#guesses').val();
	socket.emit('reveal_hint',{'room':room,'hint_word':hint_word,'guesses':guesses});
    });
    $("#leave-button").click(function(){
	socket.emit('leave',{'room':room});
    });
});
