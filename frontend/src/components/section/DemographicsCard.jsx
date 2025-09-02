function DemographicsCard({ data }) {
    if (!data || Object.keys(data).length === 0) return <p>Something is wrong. There's no demographics data</p>;
    return (
        <section className="p-4 rounded">
            <h3 className="font-semibold text-lg mb-2">Demographics/Assets Ownership</h3>
           
            <p><strong>Poverty Rate:</strong> {data.poverty_rate}</p>
            <p><strong>Mobile Phone ownership: </strong>{data.mobile_ownership}</p>
            <p><strong>Radio Ownership: </strong>{data.radio_ownership}</p>
            <p><strong>Live Stock: </strong>{data.livestock_ownership}</p>
            <p><strong>Household Electrification: </strong>{data.household_electrification}</p>
            <p><strong>Iron Sheet Roofing: </strong>{data.iron_sheet_roofing}</p>
            <p>{data.data_source}, {data.year}</p>
        </section>
    )
}

export default DemographicsCard;