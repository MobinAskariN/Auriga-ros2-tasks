#include <cmath>


// we use stanley to controll steering anlge
class Stanley_Pid{

    const int lenght {1};
    float cross_track_error{0}, heading_error{0}, kappa{0}, Steering_angle{0}, velocity {0}, curve_intensity {0};
    float k_s {0.1}; // to avoid division by zero
    //tuning constants
    float k {0};
    float k_p {0};
    

    public:

        float calculate_feed_forward_term() {return atan(lenght * kappa);}
        float calculate_steering_angle(){

            Steering_angle = heading_error + atan(k * cross_track_error / (k_s + velocity)) + calculate_feed_forward_term();

        } 

        
        void calculate_speed(){

            velocity -= (k_p * kappa);

        }

    

};


int main(){



}