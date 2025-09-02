
function StateSelector({ states, selected, onSelect }) {
  return (
    <div className="my-4">
      <select
        className="border p-2 rounded"
        onChange={onSelect}
        value={selected}
      >
        <option value="">Select a state</option>
        {states.map(state => (
          <option key={state.id} value={state.id}>
            {state.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default StateSelector;



