import DemographicsCard from './section/DemographicsCard'
import SocialUseCard from './section/SocialUseCard'
import ResourcesCard from './section/ResourcesCard'
import InfrastructureCard from './section/InfrastructureCard'

function CompareStates( { comparisonData }) {
    if (!comparisonData || comparisonData.length === 0) return null;
    return (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {comparisonData.map((profile, idx) => {
                const {state, demographics, social_uses, resources, infrastructure} = profile;
                return (
                    <div key={idx} className="border rounded p-4 shadow">
                        <h2 className="text-xl font-bold mb-4">{state.name}</h2>
                        <p><strong>Population: </strong>{state.population}</p>
                        <p><strong>Data Source: </strong>{state.data_source}, {state.year}</p>

                        <div className="grid grid-cols-1 gap-4 mt-4">
                            <DemographicsCard data={demographics}/>
                            <SocialUseCard data={social_uses} />
                            <ResourcesCard data={resources} />
                            <InfrastructureCard data={infrastructure} />
                        </div>
                    </div>
                )
            })}
        </section>
    )
}

export default CompareStates;