#include <iostream>
#include <cmath>
using namespace std;
#include <OpenEXR/ImfInputFile.h>
#include <OpenEXR/ImfOutputFile.h>
#include <OpenEXR/ImfArray.h>
#include <OpenEXR/ImfChannelList.h>
using namespace OPENEXR_IMF_NAMESPACE;
using namespace IMATH_NAMESPACE;

void ReadLayer(
		InputFile& file,
		string layer_name,
		Array2D<float>& r,
		Array2D<float>& g,
		Array2D<float>& b) {
	Box2i dw = file.header().dataWindow();
	int width = dw.max.x - dw.min.x + 1;
	int height = dw.max.y - dw.min.y + 1;

	FrameBuffer frame_buffer;

	frame_buffer.insert(
		layer_name + "R",										// name
		Slice(
			FLOAT,												// type
			(char*)(&r[0][0] - dw.min.x - dw.min.y * width),	// base
			sizeof(r[0][0]) * 1,								// xStride
			sizeof(r[0][0]) * width,							// yStride
			1, 1,												// x/y sampling
			0.0));												// fillValue

	frame_buffer.insert(
		layer_name + "G",
		Slice(
			FLOAT,
			(char*)(&g[0][0] - dw.min.x - dw.min.y * width),
			sizeof(g[0][0]) * 1,
			sizeof(g[0][0]) * width,
			1, 1,
			0.0));

	frame_buffer.insert(
		layer_name + "B",
		Slice(
			FLOAT,
			(char*)(&b[0][0] - dw.min.x - dw.min.y * width),
			sizeof(b[0][0]) * 1,
			sizeof(b[0][0]) * width,
			1, 1,
			0.0));

	file.setFrameBuffer(frame_buffer);
	file.readPixels(dw.min.y, dw.max.y);
}

void AddLayer(
		FrameBuffer& frame_buffer,
		string layer_name,
		int width, int height,
		Array2D<float>& r_,
		Array2D<float>& g_,
		Array2D<float>& b_) {
	Array2D<float> *rr = new Array2D<float>;
	Array2D<float> *gg = new Array2D<float>;
	Array2D<float> *bb = new Array2D<float>;
	Array2D<float> &r = *rr;
	Array2D<float> &g = *gg;
	Array2D<float> &b = *bb;

	r.resizeErase(height, width);
	g.resizeErase(height, width);
	b.resizeErase(height, width);
	for(int i = 0; i < height; i++)
		for(int j = 0; j < width; j++) {
			r[i][j] = r_[i][j];
			g[i][j] = g_[i][j];
			b[i][j] = b_[i][j];
		}

	frame_buffer.insert(
		layer_name + "R",				// name
		Slice(
			FLOAT,						// type
			(char*)(&r[0][0]),			// base
			sizeof(r[0][0]) * 1,		// xStride
			sizeof(r[0][0]) * width));	// yStride

	frame_buffer.insert(
		layer_name + "G",
		Slice(
			FLOAT,
			(char*)(&g[0][0]),
			sizeof(g[0][0]) * 1,
			sizeof(g[0][0]) * width));

	frame_buffer.insert(
		layer_name + "B",
		Slice(
			FLOAT,
			(char*)(&b[0][0]),
			sizeof(b[0][0]) * 1,
			sizeof(b[0][0]) * width));
}

int main(int argc, char* argv[]) {
	if(argc < 3) {
		cout << "exrmul: Multiply EXR image by a factor." << endl;
		cout << "Usage: exrmul factor input.exr output.exr" << endl;
		return 0;
	}

	float factor = atof(argv[1]);
	string input_file_path(argv[2]);
	string output_file_path(argv[3]);

	InputFile input_file(input_file_path.c_str());
	Header header = input_file.header();
	Box2i dw = header.dataWindow();
	int width = dw.max.x - dw.min.x + 1;
	int height = dw.max.y - dw.min.y + 1;

	int channel_n = 3;
	Array2D<float> channel_buffers[channel_n];
	for(int i = 0; i < channel_n; i++)
		channel_buffers[i].resizeErase(height, width);
	ReadLayer(input_file, "", channel_buffers[0], channel_buffers[1], channel_buffers[2]);
	for(int c = 0; c < channel_n; c++)
		for(int i = 0; i < height; i++)
			for(int j = 0; j < width; j++) {
				channel_buffers[c][i][j] *= factor;
				if(!std::isfinite(channel_buffers[c][i][j])) {
					cout << "Invalid pixel value!" << endl;
					exit(1);
				}
			}

	OutputFile output_file(output_file_path.c_str(), header);
	FrameBuffer frame_buffer;
	AddLayer(frame_buffer, "", width, height, channel_buffers[0], channel_buffers[1], channel_buffers[2]);
	output_file.setFrameBuffer(frame_buffer);
	output_file.writePixels(height);

	return 0;
}
