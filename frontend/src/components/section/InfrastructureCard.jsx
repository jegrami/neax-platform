
function InfrastructureCard({ data }){
    if (!data || Object.keys(data).length === 0) return <p>Something is wrong. No infra data</p> 
    return (
        <section className="p-4 rounded">
            <h3 className="font-semibold text-lg mb-2">Infrastructure</h3>
            <p><strong>Transmisson Lines &#40;length in km&#41;</strong>{data.transmisson_lines}</p>
            <p><strong>Number of Substations: </strong>{data.substations_count}</p>
            <p><strong>Minigrids: </strong>{data.mini_grids_count}</p>
            <p><strong>Off Grid Solutions: </strong>{data.off_grid_solutions}</p>
            <p><strong>Power Plants: </strong>{data.power_plants_count}</p>
            <p>{data.data_source}, {data.year}</p>

        </section>
    )
}

export default InfrastructureCard;