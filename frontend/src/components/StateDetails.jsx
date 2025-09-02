import DemographicsCard from './section/DemographicsCard'
import SocialUseCard from './section/SocialUseCard'
import ResourcesCard from './section/ResourcesCard'
import InfrastructureCard from './section/InfrastructureCard'

function StateDetails({ profile }){
    if (!profile) return null;

    const {state, demographics, social_uses, resources, infrastructure} = profile;
    return (
        <main>
            <section>
                <h2 className="text-xl font-bold mb-4">{state.name}</h2>
                <p><strong>Population: </strong>{state.population}</p>
                <p><strong>Data Source: </strong>{state.data_source} {state.year}</p>
            </section>
            <section className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <DemographicsCard data={demographics} />
                <SocialUseCard data={social_uses} />
                <ResourcesCard data={resources} />
                <InfrastructureCard data={infrastructure} />
            </section>
        </main>
    )

}

export default StateDetails;