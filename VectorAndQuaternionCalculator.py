__author__ = 'aknay'
import math
class VectorAndQuaternionCalculator:

    def getOffsetOrientationAsQuaternion(self, northAndGravityVectors):

        # accroding to paper in page 6/24
        # g = GRAVITY_VECTOR
        # gd = gravityVectorOfSensor
        # q0 = offset

        GRAVITY_VECTOR = [0.0, -1.0, 0.0]

        #GRAVITY_VECTOR = [0.0, -1.0, 0.0]
        STARTING_BYTE_OF_GRAVITY_VECTOR = 4
        gravityVectorOfSensor = northAndGravityVectors[STARTING_BYTE_OF_GRAVITY_VECTOR:]

        print "printing gravity vector"
        print gravityVectorOfSensor

        angle = self.calculateAngle(gravityVectorOfSensor, GRAVITY_VECTOR)
        print "printingAngle"
        print"Radians: %0.4f\tDegrees: %0.4f" % (angle, math.degrees(angle))

        axis = self.__vectorNormalize(self.__vectorCross(gravityVectorOfSensor, GRAVITY_VECTOR))
        print "printingAxis"
        print axis

        offset = self.__createQuaternion(axis,-angle)
        # STARTING_BYTE_OF_UNTARED_ORIENTATION_AS_QUATERNION = 1
        # taredData = self.__quaternionMultiplication(untaredOrientationAsQuaternion[STARTING_BYTE_OF_UNTARED_ORIENTATION_AS_QUATERNION:],offset)
        # print "printingTaredData"
        # print taredData
        return offset


    def getMultiplicationOfQuaternion(self,quat0,quat1):
        return self.__quaternionMultiplication(quat0,quat1)

    def getVectorOftheDeviceBasedOnSuppliedOrientation(self,vector, taredOrientationAsQuaternion, offsetAsQuaternion):
        quat = self.__quaternionMultiplication(taredOrientationAsQuaternion,offsetAsQuaternion)
        resultantVector = self.__quaternionVectorMultiplication(quat,vector)
        return resultantVector

    def calculateAngle(self,vec0, vec1, vec2=None):

        """ Calculates the angle between the two given vectors using the dot product.
        Args:
        vec0: A unit vector.
        vec1: A unit vector.
        vec2: A unit vector perpendicular to vec0 and vec1.
         """
        ## The max and min is used to account for possible floating point error
        dotProduct = max(min(self.__vectorDot(vec0, vec1), 1.0), -1.0)
        angle = math.acos(dotProduct)
        if vec2 is not None:
            print "vector printing"
            print vec0
            print vec1
            print vec2
            axis = self.__vectorNormalize(self.__vectorCross(vec0, vec1))
            angle = math.copysign(angle, self.__vectorDot(vec2, axis))
        return angle

    def __quaternionVectorMultiplication(self,quat, vec):
        """ Rotates the given vector by the given quaternion.
        Args:
            quat: A unit quaternion.
            vec: A unit vector.
        """
        ## Procedure: quat * vec_quat * -quat
        qx, qy, qz, qw = quat
        vx, vy, vz = vec
        vw = 0.0
        neg_qx = -qx
        neg_qy = -qy
        neg_qz = -qz
        neg_qw = qw
        ## First Multiply
        x_cross, y_cross, z_cross = self.__vectorCross([qx, qy, qz], vec)
        w_new = qw * vw - self.__vectorDot([qx, qy, qz], vec)
        x_new = vx * qw + qx * vw + x_cross
        y_new = vy * qw + qy * vw + y_cross
        z_new = vz * qw + qz * vw + z_cross
        ## Second Multiply
        x_cross, y_cross, z_cross = self.__vectorCross([x_new, y_new, z_new], [neg_qx, neg_qy, neg_qz])
        w = w_new * neg_qw - self.__vectorDot([x_new, y_new, z_new], [neg_qx, neg_qy, neg_qz])
        x = neg_qx * w_new + x_new * neg_qw + x_cross
        y = neg_qy * w_new + y_new * neg_qw + y_cross
        z = neg_qz * w_new + z_new * neg_qw + z_cross
        return [x, y, z]

    def __vectorDot (self,vec0, vec1):
        """ Performs the dot product on the two given vectors.
            Args:
            vec0: A unit vector.
            vec1: A unit vector.
        """
        x0, y0, z0 = vec0
        x1, y1, z1 = vec1
        return x0 * x1 + y0 * y1 + z0 * z1

    def __vectorLength(self,vec): # Calculates the length of a vector given.
        return (self.__vectorDot(vec, vec) ** 0.5)

    def __vectorNormalize(self,vec):
        """ Normalizes the vector given.
        Args:
            vec: A vector.
        """
        print "normalize"
        print vec

        length = self.__vectorLength(vec)
        x, y, z = vec
        return [x / length, y / length, z / length]

    def __vectorCross (self,vec0, vec1):
        """ Performs the cross product on the two given vectors.
        Args:
            vec0: A unit vector.
            vec1: A unit vector.
        """
        x0, y0, z0 = vec0
        x1, y1, z1 = vec1
        return [y0 * z1 - z0 * y1, z0 * x1 - x0 * z1, x0 * y1 - y0 * x1]

    def __createQuaternion(self,vec, angle):
        """ Creates a quaternion from an axis and an angle.
        Args:
            vec: A unit vector.
            angle: An angle in radians.
        """
        ## Quaternions represent half the angle in complex space so the angle must be halved
        x, y, z = vec
        tmp_quat = [0.0] * 4
        tmp_quat[0] = x * math.sin(angle / 2.0)
        tmp_quat[1] = y * math.sin(angle / 2.0)
        tmp_quat[2] = z * math.sin(angle / 2.0)
        tmp_quat[3] = math.cos(angle / 2.0)
        ## Normalize the quaternion
        qx, qy, qz, qw = tmp_quat
        length = (qx * qx + qy * qy + qz * qz + qw * qw) ** 0.5
        tmp_quat[0] /= length
        tmp_quat[1] /= length
        tmp_quat[2] /= length
        tmp_quat[3] /= length
        return tmp_quat

    def __quaternionMultiplication (self,quat0, quat1):
        """ Performs quaternion multiplication on the two given quaternions.
        Args:
            quat0: A unit quaternion.
            quat1: A unit quaternion.
        """
        x0, y0, z0, w0 = quat0
        x1, y1, z1, w1 = quat1
        x_cross, y_cross, z_cross = self.__vectorCross([x0, y0, z0], [x1, y1, z1])
        w_new = w0 * w1 - self.__vectorDot([x0, y0, z0], [x1, y1, z1])
        x_new = x1 * w0 + x0 * w1 + x_cross
        y_new = y1 * w0 + y0 * w1 + y_cross
        z_new = z1 * w0 + z0 * w1 + z_cross
        return [x_new, y_new, z_new, w_new]