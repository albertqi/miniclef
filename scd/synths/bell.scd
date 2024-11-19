SynthDef.new(\bell,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, rate=1, blur=1|
var osc, env;
sus = sus * blur;
freq = [freq, freq+fmod];
amp=(amp * 4);
osc=(Klank.ar(`[[0.501, 1, 0.7, 2.002, 3, 9.6, 2.49, 11, 2.571, 3.05, 6.242, 12.49, 13, 16, 24], [0.002, 0.1, 0.001, 0.008, 0.02, 0.004, 0.02, 0.04, 0.02, 0.005, 0.05, 0.05, 0.02, 0.03, 0.04], [1.2, 1.2, 1.2, 0.9, 0.9, 0.9, 0.25, 0.25, 0.25, 0.14, 0.14, 0.14, 0.07, 0.07, 0.07]], Impulse.ar(0.01), freq, 0, (4 * rate)) * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;