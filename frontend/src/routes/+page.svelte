<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css"

    import mapboxgl from 'mapbox-gl';
    const { Map } = mapboxgl;

    let map: any;
	let mapContainer: any;
	let lng: any, lat: any, zoom: any;

	lng = -71.224518;
	lat = 42.213995;
	zoom = 9;

	function updateData() {
    	zoom = map.getZoom();
    	lng = map.getCenter().lng;
    	lat = map.getCenter().lat;
  }

	onMount(() => {
		const initialState = { lng: lng, lat: lat, zoom: zoom };

		map = new Map({
			container: mapContainer,
			accessToken: "pk.eyJ1IjoiaGFkZXN0ZXJtaW5hbCIsImEiOiJjbHNoM2hsZGMyNDQ4MmpxbDcybGVhN3ZtIn0.NckK60v1TLPXPPNp1X_DPg",
			style: `mapbox://styles/hadesterminal/clsh3l22x03iz01p5ccl2hl9v`,
			center: [initialState.lng, initialState.lat],
			zoom: initialState.zoom,
            attributionControl: false,
		});

		map.on('move', () => {
			updateData();
		})
	});

	onDestroy(() => {
		// map.remove();
	});


    // MESSAGE STUFF BELOW ----------------------------------------
    
    let message = ""

    let data = {};

    onMount(async () => {
        fetchData();
    });

    async function fetchData() {
        try {
        const response = await fetch('http://127.0.0.1:5000/get_flight/i_want_to_go_from_houston_to_dallas_next_thursday');
        const result = await response.text();
        data = result;
        console.log(data)
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    
    

</script>





<style lang="postcss">
    .page-wrapper{
        @apply grid grid-rows-[0.5fr_6fr] h-screen;
    }
    
    .navbar{
        @apply w-full bg-neutral-700;
    }
    .navbar-wrapper{
        @apply flex flex-row justify-between w-11/12 mx-auto h-full;
        align-items: center;
    }
    .nav-link{
        @apply text-white;
    }

    .main{
        @apply h-full flex flex-col gap-2 items-center;
    }
    .top{
        @apply grid grid-cols-[8fr_3fr] gap-8 mt-8 mx-auto w-[98%] h-[80%];
    }
    .map{
        @apply w-full h-full;
    }
    .map-wrapper{
        @apply relative border border-white rounded-2xl p-8;
    }
    
    .chat-box {
        @apply border border-white rounded-2xl p-8;
    }

    .message.from-bot {
        @apply rounded-bl-none bg-gray-500 text-white px-4 py-3 rounded-xl max-w-md relative; 
    }

    
    .message.from-user {
        @apply rounded-br-none bg-gray-700 text-white px-4 py-3 rounded-xl max-w-md relative ;
    }

    .message-wrapper{
        @apply flex mb-8;
    }
    .message-wrapper:nth-child(2){
        @apply justify-end;
    }

    .bottom{
        @apply w-full;
    }

    
    .chatInput{
        @apply flex flex-row border border-white rounded-2xl p-5 w-[98%] mx-auto mt-4;
    }

    
    .circular-btn{
        @apply bg-neutral-800 text-white font-bold py-2 px-4 rounded-full ;
    }
    .circular-btn:hover{
        @apply bg-neutral-900;
    }
  

    .footer{
        @apply flex flex-row justify-center w-full bg-neutral-700 mx-auto h-full;
        align-items: center;
    }
   
    .user-input{
        @apply w-full py-2 px-4 bg-transparent rounded border-opacity-0; 
    }

    .user-input:focus{
        @apply outline-none;
    }

    .send-btn{
        @apply text-white border border-white font-bold py-2 px-4 rounded-2xl ;
    }
    .send-btn:hover{
        @apply bg-neutral-600;
    }
    .send-btn span{
        @apply text-2xl;
    }

    .map-overlay{
        @apply absolute top-0 left-0 w-full h-full flex flex-col px-10 py-12 pointer-events-auto justify-between;
    }

    .manualToggles{
        @apply h-10 w-full border border-white rounded-2xl p-8 bg-black opacity-35 backdrop-blur-2xl;
    }
    .renderedResults{
        @apply h-40 w-full overflow-x-auto whitespace-nowrap overflow-y-hidden space-x-4;
    }
    .resultCard{
        @apply h-40 w-60 border border-white rounded-2xl p-8 bg-black opacity-35 backdrop-blur-2xl inline-block;
    }
    .renderedResults ::webkit-scrollbar {
        @apply appearance-none;
    }
    
</style>

<head>
    <link href='https://api.mapbox.com/mapbox-gl-js/v3.1.2/mapbox-gl.css' rel='stylesheet' />
</head>

<section class="page-wrapper">
    <div class="navbar">
        <div class="navbar-wrapper">
            <a href="/" class="nav-link">FlightChat</a>
            <div class="helpbtn">
                <!-- Make the help button here -->
                <button class="circular-btn">Need Help?</button>
            </div>
        </div>
    </div>
    
    
    <section class="main">
        <div class="top">
            <div class="map-wrapper">
                <div class="map" bind:this={mapContainer}></div>
                <div class="map-overlay">
                    <div class="manualToggles">

                    </div>
                    <div class="renderedResults">
                        <div class="resultCard"></div>
                        <div class="resultCard"></div>
                        <div class="resultCard"></div>
                        <div class="resultCard"></div>
                        <div class="resultCard"></div>
                        <div class="resultCard"></div>
                        
                    </div>
                </div>
            </div>

            <div class="chat-box" id="chatBox">
                <div class="bot-messages">
                   
                        <div class="message-wrapper">
                            <div class="message bot-message">
                                <div class="message-text">{message}</div>
                            </div>
                        </div>
                   
                </div>
            
                <div class="user-messages">
                   
                        <div class="message-wrapper">
                            <div class="message user-message">
                                <div class="message-text">{message}</div>
                            </div>
                        </div>
                  
                </div>
            </div>

        </div>
        
        <div class="bottom">
            <div class="chatInput">
                <input type="text" id="userInput" class="user-input" placeholder="Type your message here...">
                <div class="chatSendBtn">
                    <form action="http://127.0.0.1:5000/get/flights" method="post">
                        <button class="send-btn"><span>➤</span></button>
                    </form>
                </div>
            </div>
        </div>
    </section>
</section>