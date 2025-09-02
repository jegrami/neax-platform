import { useState } from 'react';
import CompareStates from './CompareStates'

function StateComparison({ states }){
    const [a, setA] = useState('');
    const [b, setB] = useState('');
    const [comparisonData, setComparisonData] = useState([]);

    const compareStates = () => {
        if (!a || !b ) return null;
        fetch(`http://127.0.0.1:8000/api/states/compare/?a=${a}&b=${b}`)
            .then((res) => res.json())
            .then((data) => setComparisonData(data))
            .catch((err) => console.error("An error occured while trying to make comparison", err));
    };

    return (
        <section>
            <div className="flex gap-4 mb-4">
                <select value={a} onChange={(e) => setA(e.target.value)} className="border p-2 rounded">
                    <option value="">Select State A </option>
                    {states.map((state) => (
                        <option key={state.id} value={state.name}>{state.name}</option>
                    ))}

                    
                </select>

                <select value={b} onChange={(e) => setB(e.target.value)} className="border p-2 rounded">
                    <option value="">Select State B</option>
                    {states.map((state) => (
                        <option key={state.id} value={state.name}>{state.name}</option>
                    ))}
                        
                    
                </select>

                <button onClick={compareStates} className="bg-blue-600 text-white px-4 py-2 rounded"
                >
                    Compare
                </button>
            </div>

            <CompareStates comparisonData={comparisonData} />
        </section>
    )
}

export default StateComparison;