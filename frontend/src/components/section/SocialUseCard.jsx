
function SocialUseCard({ data }){
    if (!data || Object.keys(data).length === 0) return <p>Something is wrong. No social uses data</p> 
    return (
        <section className="p-4 rounded">
            <h3 className="font-semibold text-lg mb-2">Energy Use for Social Purposes</h3>
            <p><strong>Education Facilities: </strong>{data.education_facilities}</p>
            <p><strong>Health Facilities: </strong>{data.health_facilities}</p>
            <p><strong>Agricultural Zones: </strong>{data.agricultural_zones}</p>
            <p><strong>Mines and Quaries: </strong>{data.mines_quaries}</p>
            <p><strong>Commercial Activities: </strong>{data.commercial_activities}</p>
            <p><strong>Public Institutions: </strong>{data.public_institutions}</p>
            <p><strong>Nighttime Lights: </strong>{data.nighttime_lights}</p>
            <p>{data.data_source}</p>

        </section>
    )
}

export default SocialUseCard;