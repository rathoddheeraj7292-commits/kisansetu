const supabaseUrl = `https://wpmfqnobwnekpwrzwkiq.supabase.co`;
const supabaseKey = `sb_publishable_-hyFLWQE_R10fKJs_vCq5w_TjTpKTbD`;
const db = window.supabase.createClient(supabaseUrl,supabaseKey);
const tableBody = document.getElementById(`tableBody`);


async function loadMarketData(){
    const {data,error} = await db.from(`market_logs`).select(`*`);
    
    if (error){
        console.error("database error:",error);
        return;
    }
    
    let tableHtml = ``;

    data.forEach(record => {
        tableHtml +=`<tr class="hover:bg-gray-50 transition-colors border-b border-gray-200"><td class="px-6 py-4 text-sm text-gray-700">${record.id}</td><td class="px-6 py-4 text-sm font-medium text-gray-900">${record.data}</td><td class="px-6 py-4 text-sm text-gray-700">${record.price}</td><td class="px-6 py-4 text-sm text-gray-700"><button type="button" onclick="deleteRecord('${record.id}')" class="bg-red-800 text-white px-6 py-2 rounded-md hover:bg-red-400 transition-colors font-medium">delete record</button></td></tr>`;

    });
    tableBody.innerHTML = tableHtml;

}

    async function deleteRecord(recordId){
        console.log("delete button clicked with id code:",recordId);
        const {error}= await db.from(`market_logs`).delete().eq(`id`,recordId);

        if (error){
            console.error("database error:",error);
            return;
        }

        loadMarketData();

    }


loadMarketData();

const insertForm = document.getElementById(`insertForm`);
insertForm.addEventListener(`submit`,async function(e){
    e.preventDefault();
    const newEventId = document.getElementById(`eventId`).value;
    const newEventName = document.getElementById(`eventName`).value;
    const newEventPrice = parseFloat(document.getElementById(`eventPrice`).value);
    


    if (newEventPrice < 0.00){
        alert("Fatal error: price cannot be negative.");
        return;
    }

    const { error } = await db.from(`market_logs`).insert([
        {   
            id: newEventId,
            data: newEventName,
            price: newEventPrice,
            
        }
    ]);
    if (error){
        console.error("database error:",error);
        return;
    }
    insertForm.reset();
    loadMarketData();


});

