/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.hello.similarity

import java.util.HashSet
import java.util.Map
import java.util.Set

/**
 * Measures the Cosine similarity of two vectors of an inner product space and
 * compares the angle between them.
 *
 * <p>
 * For further explanation about the Cosine Similarity, refer to
 * http://en.wikipedia.org/wiki/Cosine_similarity.
 * </p>
 *
 * @since 1.0
 */
class CosineSimilarity {

    /**
     * Calculates the cosine similarity for two given vectors.
     *
     * @param leftVector left vector
     * @param rightVector right vector
     * @return cosine similarity between the two vectors
     */
    def cosineSimilarity(java.util.ArrayList leftVector, java.util.ArrayList rightVector) {
        if (leftVector == null || rightVector == null) {
            return 0.0
        }

        def dotProduct = dot(leftVector, rightVector)
        def d1 = 0.0
        for (def value : leftVector) {
            d1 += Math.pow(value, 2)
        }
        def d2 = 0.0
        for (def value : rightVector) {
            d2 += Math.pow(value, 2)
        }
        def cosSim;
        if (d1 <= 0.0 || d2 <= 0.0) {
            cosSim = 0.0
        } else {
            cosSim = (dotProduct / (Math.sqrt(d1) * Math.sqrt(d2)))
        }
        return cosSim
    }

    /**
     * Computes the dot product of two vectors. It ignores remaining elements. It means
     * that if a vector is longer than other, then a smaller part of it will be used to compute
     * the dot product.
     *
     * @param leftVector left vector
     * @param rightVector right vector
     * @param intersection common elements
     * @return the dot product
     */
    def dot(java.util.ArrayList leftVector, java.util.ArrayList rightVector) {
        def dotProduct = 0
        for (def i = 0; i < leftVector.size(); i++) {
             dotProduct += leftVector[i] * rightVector[i]
        }
        return dotProduct
    }

}

new CosineSimilarity().cosineSimilarity(left_vector, right_vector)