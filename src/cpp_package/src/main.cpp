#include <cmath>



// we use stanley to controll steering anlge
class Controller{

    const int lenght {1};
    float cross_track_error{0}, heading_error{0}, kappa{0}, Steering_angle{0}, velocity {0};
    //tuning constants
    float k {0};
    float k_p {0};
    float k_ff {0};
    

    public:
    
        float calculate_steering_angle(){

            velocity = std::max(velocity, 0.001f); // to avoid division by zero
            Steering_angle = heading_error + atan(k * cross_track_error / (velocity)) +  k_ff * atan(lenght * kappa);

        } 

    

};


int main(){



}