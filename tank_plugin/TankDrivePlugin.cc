#include <gz/sim/System.hh>
#include <gz/plugin/Register.hh>
#include <sdf/Element.hh>
#include <gz/sim/Model.hh>
#include <gz/transport/Node.hh>
#include <gz/msgs/vector2d.pb.h>
#include <gz/sim/EntityComponentManager.hh>
#include <gz/sim/components/JointVelocityCmd.hh>
#include <gz/sim/Types.hh>

#include <cmath>
#include <iostream>
#include <memory>
#include <string>

using namespace gz;
using namespace sim;

class TankDrivePlugin :
    public System,
    public ISystemConfigure,
    public ISystemPreUpdate
{
public:
    void Configure(
        const Entity &_entity,
        const std::shared_ptr<const sdf::Element> &_sdf,
        EntityComponentManager & _ecm,
        EventManager &) override
    {
        this->model = Model(_entity);
        this->modelEntity = _entity; 
        this->leftFrontJoint = 
            this->model.JointByName(_ecm, "left_wheel_joint");
        this->leftBackJoint =
            this->model.JointByName(_ecm, "back_left_wheel_joint");
        this->rightFrontJoint = 
            this->model.JointByName(_ecm, "right_wheel_joint");
        this->rightBackJoint =
            this->model.JointByName(_ecm, "back_right_wheel_joint");
        
        std::cout << "Model entity ID: " << this->modelEntity << std::endl;
        std::cout << "LF entity ID: " << this->leftFrontJoint << std::endl; //if not zero, joint found 
        std::cout << "LB entity ID: " << this->leftBackJoint << std::endl;
        std::cout << "RF entity ID: " << this->rightFrontJoint << std::endl;
        std::cout << "LB entity ID: " << this->rightBackJoint << std::endl;

        if (_sdf->HasElement("topic")){
            this->topic =
                _sdf->Get<std::string>("topic");
        }

        if(_sdf->HasElement("rpm")){
            this->rpm =
                _sdf->Get<double>("rpm"); 
        }

        std::cout << "recieved rpm: " << rpm << std::endl;

        this->node.Subscribe(topic, &TankDrivePlugin::OnCmd, this);
        std::cout << "Subscribed to " << this->topic<< std::endl;

        std::cout << "TankDrivePlugin loaded!" << std::endl;
    }

    void OnCmd(const gz::msgs::Vector2d &_msg)
    {
        this->leftVoltageCmd = _msg.x();
        this->rightVoltageCmd = _msg.y();

        // std::cout << "Left: " << this->leftVoltage
        //         << " Right: " << this->rightVoltage
        //         << std::endl;
    }

    void PreUpdate(
        const UpdateInfo &,
        EntityComponentManager &_ecm) override
    {
        double maxSpeedRad = rpm * 2 * M_PI / 60.0; 

        double targetLeftSpeed = (leftVoltageCmd / 12.0) * maxSpeedRad;
        double targetRightSpeed = (rightVoltageCmd / 12.0) * maxSpeedRad;

        this->leftWheelSpeed += (targetLeftSpeed - this->leftWheelSpeed) * 0.02;
        this->rightWheelSpeed += (targetRightSpeed - this->rightWheelSpeed) * 0.02;

        this->SetJointVelocity(_ecm, this->leftFrontJoint, leftWheelSpeed);
        this->SetJointVelocity(_ecm, this->leftBackJoint, leftWheelSpeed);
        this->SetJointVelocity(_ecm, this->rightFrontJoint, rightWheelSpeed);
        this->SetJointVelocity(_ecm, this->rightBackJoint, rightWheelSpeed);
    }

    void SetJointVelocity(
        EntityComponentManager &_ecm,
        Entity _joint,
        double _speed)
    {
        if (_joint == kNullEntity){
            return;
        }

        auto comp =
            _ecm.Component<components::JointVelocityCmd>(_joint);

        if (!comp)
        {
            _ecm.CreateComponent(
                _joint,
                components::JointVelocityCmd({_speed}));
            // std::cout << "Successfully created component!" << std::endl; 
        }
        else
        {
            comp->Data()[0] = _speed;
            // std::cout << "Successfully set speed!" << std::endl;
        }
    }
private:
    Model model{kNullEntity};
    Entity modelEntity = kNullEntity; 

    Entity leftFrontJoint{kNullEntity};
    Entity leftBackJoint{kNullEntity};
    Entity rightFrontJoint{kNullEntity};
    Entity rightBackJoint{kNullEntity};

    double leftVoltageCmd = 0.0;
    double rightVoltageCmd = 0.0;
    double leftWheelSpeed = 0.0;
    double rightWheelSpeed = 0.0;
    double rpm = 600; 

    gz::transport::Node node;

    std::string topic = "/tank_cmd";
};

GZ_ADD_PLUGIN(
    TankDrivePlugin,
    System,
    TankDrivePlugin::ISystemConfigure,
    TankDrivePlugin::ISystemPreUpdate
)
