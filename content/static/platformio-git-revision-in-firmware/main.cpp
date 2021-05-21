#ifndef UNIT_TEST

#include <Arduino.h>

#ifndef SRC_REVISION
#define SRC_REVISION "(revision not defined)"
#endif

#ifndef SRC_STATE
#define SRC_STATE "(state not defined)"
#endif

void setup() {
    Serial.begin(115200);
}

void loop()
{
    Serial.println(SRC_REVISION);
    Serial.println(SRC_STATE);
    Serial.println();

    delay(1000);
}

#endif
