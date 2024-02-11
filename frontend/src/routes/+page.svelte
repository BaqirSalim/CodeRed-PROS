<script lang="ts">
    import { onMount, onDestroy } from "svelte";

    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css"
    import mapboxgl from 'mapbox-gl';

    import { createEventDispatcher } from 'svelte';
    
    const { Map } = mapboxgl;

    let map: any;
	let mapContainer: any;
	let lng: any, lat: any, zoom: any;

	lng = -71.224518;
	lat = 42.21395;
	zoom = 3;

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

        addMarker()
	});

    function addMarker(){
        const apiKey = '3b4366a54f270d8cc0b772fcfc66b383';
        const iataCode = 'LAX';

        fetch(`https://api.aviationstack.com/v1/airports?access_key=${apiKey}&iata_code=${iataCode}`)
        .then(response => response.json())
        .then(data => {
            const longitude = data.data[0].longitude;
            const latitude = data.data[0].latitude;
            console.log(`Longitude: ${longitude}, Latitude: ${latitude}`);
        })
        .catch(error => console.error('Error:', error));
    }


    const dispatch = createEventDispatcher();


    let isModalOpen = false;

    function handleClick() {
        isModalOpen = true;
        dispatch('toggleModal');
    }

    function closeModal() {
        isModalOpen = false;
    }
    
    // MESSAGE STUFF BELOW ----------------------------------------
    
    let message = ""
    let conversation = [
        {
            role : "agent",
            message : "Hey there, how may I help you today?"
        },
    ]

    async function addToConversation(){
        conversation = [...conversation, {role : "user", message : message}];

        //displayLoadingMessage(); // Display loading message

        fetchData(message)
		message = '';
        console.log(conversation)
    }

    async function fetchData(message: string) {

        // let response = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        // conversation = [...conversation, {role : "agent", message : response}];

        try {
            const response = await fetch(`http://127.0.0.1:5000/get_flight/${encodeURIComponent(message)}`);
            const responseData = await response.json(); // Assuming the response is in JSON format
            
            conversation = [...conversation, {role : "agent", message : responseData.naturalResponse}];
            console.log(responseData);
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
        @apply w-full bg-neutral-700 h-[75px];
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
        @apply relative border border-white rounded-2xl p-8 max-h-[740px];
    }
    
    .chat-box {
        @apply max-h-[750px] h-full border border-white rounded-2xl p-8 overflow-y-scroll;
    }
    .chat-box::-webkit-scrollbar{
        @apply w-3 ;
    }
    .chat-box::-webkit-scrollbar{
        -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
        border-radius: 10px;
    }

    .message.from-bot {
        @apply rounded-bl-none bg-gray-500 text-white px-4 py-3 rounded-xl max-w-md relative; 
    }

    
    .message.from-user {
        @apply rounded-br-none bg-gray-700 text-white px-4 py-3 rounded-xl max-w-md relative self-end;
    }

    .message-wrapper{
        @apply flex mb-8;
    }
    .message-wrapper:nth-child(2n){
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

    .modal-wrapper{
        @apply fixed top-0 left-0 w-screen h-screen flex justify-center items-center bg-black bg-opacity-50 z-50;
    }
    .modal{
        @apply w-4/6 h-4/6 bg-white p-8 rounded-3xl;
    }
    .modal button{
        @apply flex justify-end;
    }
    .modal-close{
        @apply w-full flex flex-col justify-end;
    }

    .modal-close span{
        @apply text-black text-3xl ;
    }

    .modal-close p{
        @apply text-black text-xl;
    }
    .modal-text{
        @apply flex pt-8 my-auto gap-6 flex-col;
    }


    .message{
        @apply bg-gray-400; 
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
        @apply absolute top-0 left-0 w-full h-full flex flex-col px-10 py-12 pointer-events-none justify-between;
    }

    .flightInfo{
        @apply h-full w-4/12 border border-white rounded-2xl p-8 bg-black opacity-35 backdrop-blur-2xl;
    }

    .modal-text > p > a{
        @apply underline;
    }

    .modal-wrapper {
        @apply fixed inset-0 flex items-center justify-center;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 9999; /* Ensure the modal is on top */
    }

    .modal {
        @apply bg-white p-4 rounded-lg shadow-lg;
        width: 80%;
        max-width: 600px;
    }

    .modal-close {
        @apply flex justify-end;
    }

</style>

<head>
    <link href='https://api.mapbox.com/mapbox-gl-js/v3.1.2/mapbox-gl.css' rel='stylesheet' />
</head>

<section class="page-wrapper">
    <div class="navbar">
        <div class="navbar-wrapper">
            <a href="/" class="nav-link">
                <svg width="207" height="44" viewBox="0 0 207 44" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M52.849 4.00563L44.8509 41.344C44.2475 43.9792 42.674 44.6351 40.4378 43.3936L28.2515 34.5041L22.3713 40.1025C21.7205 40.7466 21.1763 41.2854 19.9222 41.2854L20.7977 28.9994L43.3839 8.7959C44.3659 7.9292 43.1709 7.449 41.8576 8.3157L13.9355 25.72L1.91475 21.9955C-0.699985 21.1874 -0.747311 19.4071 2.459 18.1656L49.477 0.234313C51.654 -0.573825 53.5589 0.714512 52.849 4.00563Z" fill="white"/>
                    <path d="M58.05 30L62.04 14.67H64.581L68.55 30H66.639L65.631 25.926H60.99L59.982 30H58.05ZM61.368 24.33H65.232L64.056 19.605C63.832 18.709 63.657 17.96 63.531 17.358C63.405 16.756 63.328 16.364 63.3 16.182C63.272 16.364 63.195 16.756 63.069 17.358C62.943 17.96 62.768 18.702 62.544 19.584L61.368 24.33Z" fill="white"/>
                    <path d="M71.6918 30V14.67H80.5118V16.392H73.5608V21.138H79.7768V22.839H73.5608V28.278H80.5118V30H71.6918Z" fill="white"/>
                    <path d="M84.1156 30V14.67H88.8616C89.7716 14.67 90.5696 14.859 91.2556 15.237C91.9416 15.601 92.4736 16.112 92.8516 16.77C93.2296 17.428 93.4186 18.198 93.4186 19.08C93.4186 20.116 93.1456 21.005 92.5996 21.747C92.0676 22.489 91.3396 23 90.4156 23.28L93.6286 30H91.4026L88.4626 23.49H86.0056V30H84.1156ZM86.0056 21.789H88.8616C89.6456 21.789 90.2756 21.544 90.7516 21.054C91.2276 20.55 91.4656 19.892 91.4656 19.08C91.4656 18.254 91.2276 17.596 90.7516 17.106C90.2756 16.616 89.6456 16.371 88.8616 16.371H86.0056V21.789Z" fill="white"/>
                    <path d="M101.075 30.21C100.151 30.21 99.3534 30.035 98.6814 29.685C98.0234 29.335 97.5124 28.831 97.1484 28.173C96.7984 27.501 96.6234 26.71 96.6234 25.8V18.87C96.6234 17.946 96.7984 17.155 97.1484 16.497C97.5124 15.839 98.0234 15.335 98.6814 14.985C99.3534 14.635 100.151 14.46 101.075 14.46C101.999 14.46 102.79 14.635 103.448 14.985C104.12 15.335 104.631 15.839 104.981 16.497C105.345 17.155 105.527 17.939 105.527 18.849V25.8C105.527 26.71 105.345 27.501 104.981 28.173C104.631 28.831 104.12 29.335 103.448 29.685C102.79 30.035 101.999 30.21 101.075 30.21ZM101.075 28.509C101.901 28.509 102.531 28.278 102.965 27.816C103.413 27.34 103.637 26.668 103.637 25.8V18.87C103.637 18.002 103.413 17.337 102.965 16.875C102.531 16.399 101.901 16.161 101.075 16.161C100.263 16.161 99.6334 16.399 99.1854 16.875C98.7374 17.337 98.5134 18.002 98.5134 18.87V25.8C98.5134 26.668 98.7374 27.34 99.1854 27.816C99.6334 28.278 100.263 28.509 101.075 28.509Z" fill="white"/>
                    <path d="M121.555 30V14.67H124.033L125.629 19.626C125.783 20.074 125.923 20.522 126.049 20.97C126.175 21.404 126.266 21.74 126.322 21.978C126.392 21.74 126.483 21.404 126.595 20.97C126.707 20.522 126.833 20.067 126.973 19.605L128.485 14.67H130.963V30H129.115V24.435C129.115 23.819 129.136 23.119 129.178 22.335C129.22 21.551 129.276 20.753 129.346 19.941C129.416 19.115 129.486 18.331 129.556 17.589C129.64 16.833 129.71 16.175 129.766 15.615L127.288 23.28H125.293L122.794 15.615C122.864 16.161 122.934 16.798 123.004 17.526C123.074 18.24 123.137 19.003 123.193 19.815C123.249 20.613 123.298 21.411 123.34 22.209C123.382 23.007 123.403 23.749 123.403 24.435V30H121.555Z" fill="white"/>
                    <path d="M133.601 30L137.591 14.67H140.132L144.101 30H142.19L141.182 25.926H136.541L135.533 30H133.601ZM136.919 24.33H140.783L139.607 19.605C139.383 18.709 139.208 17.96 139.082 17.358C138.956 16.756 138.879 16.364 138.851 16.182C138.823 16.364 138.746 16.756 138.62 17.358C138.494 17.96 138.319 18.702 138.095 19.584L136.919 24.33Z" fill="white"/>
                    <path d="M147.243 30V14.67H156.063V16.392H149.112V21.138H155.328V22.839H149.112V28.278H156.063V30H147.243Z" fill="white"/>
                    <path d="M164.118 30.21C163.11 30.21 162.242 30.042 161.514 29.706C160.8 29.37 160.247 28.887 159.855 28.257C159.463 27.627 159.26 26.878 159.246 26.01H161.136C161.136 26.78 161.395 27.389 161.913 27.837C162.445 28.285 163.18 28.509 164.118 28.509C165 28.509 165.686 28.292 166.176 27.858C166.68 27.424 166.932 26.822 166.932 26.052C166.932 25.436 166.764 24.897 166.428 24.435C166.106 23.973 165.637 23.651 165.021 23.469L162.942 22.818C161.892 22.496 161.08 21.957 160.506 21.201C159.946 20.445 159.666 19.556 159.666 18.534C159.666 17.708 159.848 16.994 160.212 16.392C160.59 15.776 161.115 15.3 161.787 14.964C162.459 14.614 163.25 14.439 164.16 14.439C165.504 14.439 166.582 14.817 167.394 15.573C168.206 16.315 168.619 17.309 168.633 18.555H166.743C166.743 17.799 166.512 17.211 166.05 16.791C165.602 16.357 164.965 16.14 164.139 16.14C163.327 16.14 162.69 16.336 162.228 16.728C161.78 17.12 161.556 17.666 161.556 18.366C161.556 18.996 161.724 19.542 162.06 20.004C162.396 20.466 162.879 20.795 163.509 20.991L165.609 21.663C166.631 21.985 167.422 22.531 167.982 23.301C168.542 24.071 168.822 24.974 168.822 26.01C168.822 26.85 168.626 27.585 168.234 28.215C167.842 28.845 167.289 29.335 166.575 29.685C165.875 30.035 165.056 30.21 164.118 30.21Z" fill="white"/>
                    <path d="M175.681 30V16.371H171.481V14.649H181.771V16.371H177.571V30H175.681Z" fill="white"/>
                    <path d="M184.85 30V14.67H189.596C190.506 14.67 191.304 14.859 191.99 15.237C192.676 15.601 193.208 16.112 193.586 16.77C193.964 17.428 194.153 18.198 194.153 19.08C194.153 20.116 193.88 21.005 193.334 21.747C192.802 22.489 192.074 23 191.15 23.28L194.363 30H192.137L189.197 23.49H186.74V30H184.85ZM186.74 21.789H189.596C190.38 21.789 191.01 21.544 191.486 21.054C191.962 20.55 192.2 19.892 192.2 19.08C192.2 18.254 191.962 17.596 191.486 17.106C191.01 16.616 190.38 16.371 189.596 16.371H186.74V21.789Z" fill="white"/>
                    <path d="M201.81 30.21C200.886 30.21 200.088 30.035 199.416 29.685C198.758 29.335 198.247 28.831 197.883 28.173C197.533 27.501 197.358 26.71 197.358 25.8V18.87C197.358 17.946 197.533 17.155 197.883 16.497C198.247 15.839 198.758 15.335 199.416 14.985C200.088 14.635 200.886 14.46 201.81 14.46C202.734 14.46 203.525 14.635 204.183 14.985C204.855 15.335 205.366 15.839 205.716 16.497C206.08 17.155 206.262 17.939 206.262 18.849V25.8C206.262 26.71 206.08 27.501 205.716 28.173C205.366 28.831 204.855 29.335 204.183 29.685C203.525 30.035 202.734 30.21 201.81 30.21ZM201.81 28.509C202.636 28.509 203.266 28.278 203.7 27.816C204.148 27.34 204.372 26.668 204.372 25.8V18.87C204.372 18.002 204.148 17.337 203.7 16.875C203.266 16.399 202.636 16.161 201.81 16.161C200.998 16.161 200.368 16.399 199.92 16.875C199.472 17.337 199.248 18.002 199.248 18.87V25.8C199.248 26.668 199.472 27.34 199.92 27.816C200.368 28.278 200.998 28.509 201.81 28.509Z" fill="white"/>
                </svg>                    
            </a>
            <div class="helpbtn">
                <!-- Make the help button here -->
                <button class="circular-btn" on:click={handleClick}>Project Info</button>
            </div>
        </div>
    </div>
    
    
    <section class="main">
        <div class="top">
            <div class="map-wrapper">
                <div class="map" bind:this={mapContainer}></div>
                <!-- <div class="map-overlay">
                    <div class="flightInfo">

                    </div>
                </div> -->
            </div>

            <div class="chat-box" id="chatBox">
                {#each conversation as { role, message }}
                    {#if role === 'agent'}
                        <div class="message-wrapper">
                            <div class="message from-bot">
                                <div class="message-text">{message}</div>
                            </div>
                        </div>
                    {:else if role === 'user'}
                        <div class="message-wrapper">
                            <div class="message from-user">
                                <div class="message-text">{message}</div>
                            </div>
                        </div>
                    {/if}
                {/each}
            </div>

        </div>
        
        <div class="bottom">
            <div class="chatInput">
                <input type="text" id="userInput" bind:value={message} class="user-input" placeholder="Type your message here...">
                <div class="chatSendBtn">
                    <button  on:click={addToConversation} class="send-btn"><span>➤</span></button>
                </div>
            </div>
        </div>
        
    </section>
</section>

{#if isModalOpen}
<div class="modal-wrapper">
    <div class="modal">
        <div class="modal-close">
            <button on:click={closeModal} class=""><span>✖</span></button>
            <div class="modal-text">
                <p>Welcome to AeroMaestro!</p>
                <p>AeroMaestro is an innovative airline geolocation site that offers users the ability to calculate flight durations between any two cities worldwide, regardless of the country you're in. Whether you're planning a business trip, a vacation, or simply curious about travel times, Flight Chat provides accurate and efficient flight duration estimates.-webkit-scrollbar</p>
                <p>By leveraging advanced geolocation technology and comprehensive airline databases, AeroMaestro enables travelers to quickly and conveniently determine the time it would take to fly from one destination to another. Our platform empowers users to make informed travel decisions, optimize their itineraries, and enhance their overall travel experiences.</p>  
                <p>This project was made by <a href="https://github.com/matthewyohannes" target="_blank" class="card-link">Matthew Yohannes</a>, <a href="https://github.com/JoshuaEworo" target="_blank" class="card-link">Joshua Eworo</a>, <a href="https://github.com/BaqirSalim" target="_blank" class="card-link">Baqir Salim</a>, and <a href="https://github.com/Akashew" target="_blank" class="card-link">Akash Nelson</a>.</p>
            </div>
        </div>
    </div>
</div>
{/if}