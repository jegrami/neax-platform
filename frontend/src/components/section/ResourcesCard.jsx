
function ResourcesCard({ data }){
    if (!data || Object.keys(data).length === 0) return <p>Something is wrong. No Resource data</p> 
    return (
        <section className="p-4 rounded">
            <h3 className="font-semibold text-lg mb-2">Energy Resources/Potential</h3>
            <p><strong>Solar: </strong>{data.solar_potential}</p>
            <p><strong>Wind: </strong>{data.wind_potential}</p>
            <p><strong>Biomass Potential: </strong>{data.biomass_potential}</p>
            <p><strong>Hydro: </strong>{data.hydro_potential}</p>
            <p>{data.data_source}, {data.year}</p>

        </section>
    )
}

export default ResourcesCard;
