
import { useState, useEffect } from 'react'
import StateDetails from '../components/StateDetails'
import StateComparison from '../components/StateComparison'
import StateSelector from  '../components/StateSelector'



function DataExplorer() {
    const [states, setStates] = useState([]);
    const [selected, setSelected] = useState("");
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/states')
            .then((res) => res.json())
            .then((data) => setStates(data));
    }, []);

    async function handleStateSelection(event){
        const stateId = event.target.value;
        setSelected(stateId);
        const res = await fetch(`http://127.0.0.1:8000/api/states/${stateId}/full/`);
        const data = await res.json();
        setProfile(data);
    }

    return (
        <main>
            <section className="bg-white rounded-lg p-4 shadow">
                <h2 className="text-xl font-semibold mb-4">Explore Nigeria's Energy Data by State</h2>
                <StateSelector states={states} 
                        selected={selected} 
                        onSelect={handleStateSelection}
                />

                <StateDetails profile={profile} />

            </section>
            
            <section className="bg-white rounded-lg p-4 shadow mt-6">
                <h2 className="text-xl font-semibold mb-4">Compare two States</h2>
                <StateComparison states={states} />
            </section>
        </main>
    )
}
   
export default DataExplorer;
