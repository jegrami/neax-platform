import { useState, useRef, useEffect } from 'react'

function scrollAnimation() {
    const [isVisible, setIsVisible] = useState(false);
    const ref = useRef(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                } 
                
            },
            {threshold: 0.2}
        );

        if (ref.current){
            observer.observe(ref.current);
        }
        return () => observer.disconnect();

    }, [])

    return {ref, isVisible};
}

export default scrollAnimation;
